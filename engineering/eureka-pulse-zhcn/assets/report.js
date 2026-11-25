const root = document.documentElement;
const progressBar = document.getElementById('reading-progress-bar');
let progressPending = false;
function updateReadingProgress() {
  const distance = root.scrollHeight - innerHeight;
  progressBar.style.transform = 'scaleX(' + (distance > 0 ? Math.min(1, Math.max(0, scrollY / distance)) : 0) + ')';
  progressPending = false;
}
window.addEventListener('scroll', () => {
  if (!progressPending) {
    progressPending = true;
    requestAnimationFrame(updateReadingProgress);
  }
}, { passive: true });
window.addEventListener('resize', updateReadingProgress);
window.addEventListener('load', updateReadingProgress);
updateReadingProgress();
document.getElementById('print-button').addEventListener('click', () => window.print());
const recordGroups = new Map();
function updateRecordGroup(state, visibleCount) {
  const positions = new Map(state.matchingCards.map((card, index) => [card, index]));
  state.visibleCount = Math.min(visibleCount, state.matchingCards.length);
  state.list.dataset.visibleCount = String(state.visibleCount);
  state.cards.forEach(card => { card.hidden = !state.enabled || !positions.has(card) || positions.get(card) >= state.visibleCount; });
  if (state.button) state.button.hidden = !state.enabled || state.visibleCount >= state.matchingCards.length;
}
for (const list of document.querySelectorAll('[data-record-group]')) {
  const cards = [...list.children].filter(node => node.matches('article.record'));
  const initial = Number(list.dataset.initialVisible);
  const step = Number(list.dataset.loadStep);
  const next = list.nextElementSibling;
  const button = next?.matches('[data-record-more]') && next.getAttribute('aria-controls') === list.id ? next : null;
  if (!Number.isInteger(initial) || initial < 1 || !Number.isInteger(step) || step < 1 ||
      (cards.length > initial && !button)) throw new Error('子目录展示设置或查看更多入口无效');
  const state = { list, cards, matchingCards: cards, enabled: true, button, step, initial, visibleCount: 0 };
  recordGroups.set(list, state);
  updateRecordGroup(state, initial);
  if (button) button.addEventListener('click', () => {
    const firstNew = state.matchingCards[state.visibleCount];
    updateRecordGroup(state, state.visibleCount + state.step);
    if (firstNew) {
      const focusTarget = firstNew.querySelector('.record-open, .record-details > summary') || firstNew;
      if (focusTarget === firstNew) firstNew.tabIndex = -1;
      focusTarget.focus({ preventScroll: true });
      firstNew.scrollIntoView({ block: 'start', behavior: 'instant' });
    }
  });
}
function revealRecordTarget(target) {
  const wrapper = target?.closest('[data-report-group]');
  const groupState = recordGroups.get(wrapper?.querySelector('[data-record-group]'));
  if (groupState && (!groupState.enabled || groupState.matchingCards.length !== groupState.cards.length)) groupState.resetFilters?.();
  const card = target?.closest('article.record');
  const state = card && recordGroups.get(card.parentElement);
  if (!state || !card.hidden) return;
  const index = state.matchingCards.indexOf(card);
  const batches = Math.ceil((index + 1 - state.visibleCount) / state.step);
  updateRecordGroup(state, state.visibleCount + batches * state.step);
}
for (const image of document.querySelectorAll('figure img')) {
  function showFailure() {
    image.hidden = true;
    image.closest('figure').querySelector('.image-error, figcaption').hidden = false;
    if (!image.closest('.selected-figures')) image.closest('.record-layout')?.classList.remove('with-image');
  }
  image.addEventListener('error', showFailure);
  if (image.complete && image.naturalWidth === 0) showFailure();
}
const drawer = document.getElementById('record-drawer');
const drawerBody = document.getElementById('record-drawer-body');
const citationList = document.getElementById('record-citation-list');
const drawerBack = document.getElementById('drawer-back');
const imagePreview = document.getElementById('image-preview');
let previewImage = null;
function hideImagePreview() {
  previewImage = null;
  imagePreview.hidden = true;
  imagePreview.replaceChildren();
}
function showImagePreview(image) {
  if (!image.complete || image.naturalWidth === 0) return;
  previewImage = image;
  const host = drawer.contains(image) ? drawer : document.body;
  host.append(imagePreview);
  const enlarged = image.cloneNode(false);
  enlarged.hidden = false;
  enlarged.removeAttribute('loading');
  enlarged.alt = '';
  imagePreview.replaceChildren(enlarged);
  imagePreview.hidden = false;
  const bounds = image.getBoundingClientRect();
  const width = imagePreview.offsetWidth;
  const height = imagePreview.offsetHeight;
  const right = bounds.right + 16;
  const left = right + width <= innerWidth - 16 ? right : bounds.left - width - 16;
  imagePreview.style.left = Math.max(16, Math.min(innerWidth - width - 16, left)) + 'px';
  imagePreview.style.top = Math.max(16, Math.min(innerHeight - height - 16, bounds.top)) + 'px';
}
for (const image of document.querySelectorAll('figure img')) {
  image.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') showImagePreview(image);
  });
  image.addEventListener('pointerleave', hideImagePreview);
  const link = image.closest('a');
  if (link) {
    link.addEventListener('focus', () => showImagePreview(image));
    link.addEventListener('blur', hideImagePreview);
  }
}
window.addEventListener('scroll', event => {
  if (!previewImage) return;
  const pageScroll = event.target === document || event.target === window;
  if (pageScroll ? !drawer.contains(previewImage) : event.target instanceof Element && event.target.contains(previewImage)) hideImagePreview();
}, true);
window.addEventListener('resize', hideImagePreview);
let activeRecord = null;
let activeCitationList = null;
function restoreRecordSource() {
  if (activeRecord) activeRecord.card.append(activeRecord.source);
}
function showCitationList(restoreFocus = false) {
  if (!activeCitationList) throw new Error('引用列表缺少资料');
  hideImagePreview();
  if (activeRecord) activeRecord.trigger.setAttribute('aria-expanded', 'false');
  restoreRecordSource();
  activeRecord = null;
  citationList.hidden = false;
  drawerBack.hidden = true;
  document.getElementById('record-drawer-label').textContent = '本期概述引用';
  document.getElementById('record-drawer-title').textContent = activeCitationList.label + '（' + activeCitationList.cards.length + '条）';
  activeCitationList.trigger.setAttribute('aria-expanded', 'true');
  root.classList.add('drawer-open');
  if (!drawer.open) drawer.showModal();
  drawerBody.scrollTop = activeCitationList.scrollTop;
  const target = restoreFocus && activeCitationList.focusItem ? activeCitationList.focusItem : document.getElementById('drawer-close');
  target.focus({ preventScroll: true });
}
function openCitationList(trigger) {
  const cards = trigger.dataset.recordTargets.split(' ').map(identity => {
    const card = document.getElementById(identity);
    if (!card) throw new Error('引用列表包含不存在的资料');
    return card;
  });
  if (!cards.length || new Set(cards).size !== cards.length || Number(trigger.dataset.citationCount) !== cards.length) throw new Error('引用数量与资料列表不一致');
  const focusTarget = activeCitationList?.focusTarget || activeRecord?.focusTarget || trigger;
  if (activeRecord) activeRecord.trigger.setAttribute('aria-expanded', 'false');
  restoreRecordSource();
  activeRecord = null;
  const types = new Set(cards.map(card => card.querySelector('.record-kind').textContent));
  const label = (types.size === 1 ? [...types][0] : '资料') + '列表';
  activeCitationList = { trigger, cards, label, focusTarget, focusItem: null, scrollTop: 0 };
  const list = document.createElement('ol');
  list.className = 'citation-records';
  for (const card of cards) {
    const item = document.createElement('li');
    item.className = 'citation-record-entry';
    item.dataset.recordTarget = card.id;
    const button = document.createElement('button');
    button.className = 'citation-record-open';
    button.type = 'button';
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-controls', 'record-drawer');
    button.setAttribute('aria-expanded', 'false');
    button.append(card.querySelector('.record-kind').cloneNode(true), card.querySelector('.record-title').cloneNode(true));
    button.addEventListener('click', () => openRecord(card, button));
    const metadata = card.querySelector(':scope > .record-meta').cloneNode(true);
    metadata.classList.add('citation-record-meta');
    item.append(button, metadata);
    const summarySource = card.querySelector(':scope > template.citation-summary-source');
    if (summarySource) {
      const summary = document.createElement('div');
      summary.className = 'citation-record-summary rich-text';
      summary.dataset.fieldKey = summarySource.dataset.fieldKey;
      summary.append(summarySource.content.cloneNode(true));
      item.append(summary);
    }
    list.append(item);
  }
  citationList.replaceChildren(list);
  drawerBack.textContent = '返回' + label;
  showCitationList();
}
function openRecord(card, trigger) {
  hideImagePreview();
  const source = document.getElementById(card.dataset.detailTarget);
  if (!source || !trigger) throw new Error('资料抽屉缺少对应内容或打开入口');
  const focusTarget = activeRecord?.focusTarget || activeCitationList?.focusTarget || trigger;
  if (activeCitationList && citationList.contains(trigger)) {
    activeCitationList.focusItem = trigger;
    activeCitationList.scrollTop = drawerBody.scrollTop;
  }
  if (activeRecord) {
    activeRecord.trigger.setAttribute('aria-expanded', 'false');
    restoreRecordSource();
  }
  activeRecord = { card, source, trigger, focusTarget };
  citationList.hidden = true;
  drawerBack.hidden = !activeCitationList;
  document.getElementById('record-drawer-label').textContent = card.querySelector('.record-kind').textContent + '详细资料';
  document.getElementById('record-drawer-title').textContent = card.querySelector('.record-title').textContent;
  drawerBody.append(source);
  drawerBody.scrollTop = 0;
  trigger.setAttribute('aria-expanded', 'true');
  root.classList.add('drawer-open');
  if (!drawer.open) drawer.showModal();
  document.getElementById('drawer-close').focus({ preventScroll: true });
}
for (const citation of document.querySelectorAll('a.citation-link')) {
  const card = document.getElementById(citation.dataset.recordTarget);
  if (!card) throw new Error('引用资料不存在');
  citation.title = citation.getAttribute('aria-label') + '：' + card.querySelector('.record-title').textContent;
  citation.setAttribute('aria-label', citation.title);
}
for (const citation of document.querySelectorAll('a.citation-group-link')) {
  citation.title = citation.getAttribute('aria-label');
}
document.addEventListener('click', event => {
  const group = event.target.closest('a.citation-group-link');
  if (group) {
    event.preventDefault();
    openCitationList(group);
    return;
  }
  const citation = event.target.closest('a.citation-link');
  if (!citation) return;
  event.preventDefault();
  openRecord(document.getElementById(citation.dataset.recordTarget), citation);
});
document.addEventListener('keydown', event => {
  const citation = event.target.closest('a.citation-link, a.citation-group-link');
  if (citation && event.key === ' ') {
    event.preventDefault();
    citation.click();
  }
});
for (const card of document.querySelectorAll('.record-patent')) {
  card.addEventListener('click', event => {
    const control = event.target.closest('a, button, summary, input, select, textarea');
    if (control && !control.classList.contains('record-open')) return;
    if (!control && window.getSelection().toString().trim()) return;
    openRecord(card, card.querySelector('.record-open'));
  });
}
function finishRecord() {
  if ((!activeRecord && !activeCitationList) || drawer.open) return;
  const focusTarget = activeCitationList?.focusTarget || activeRecord.focusTarget;
  restoreRecordSource();
  root.classList.remove('drawer-open');
  if (activeRecord) activeRecord.trigger.setAttribute('aria-expanded', 'false');
  if (activeCitationList) activeCitationList.trigger.setAttribute('aria-expanded', 'false');
  activeRecord = null;
  activeCitationList = null;
  citationList.hidden = true;
  citationList.replaceChildren();
  drawerBack.hidden = true;
  focusTarget.focus({ preventScroll: true });
}
function closeRecord() {
  hideImagePreview();
  drawer.close();
  finishRecord();
}
document.getElementById('drawer-close').addEventListener('click', closeRecord);
drawerBack.addEventListener('click', () => showCitationList(true));
drawer.addEventListener('cancel', event => {
  event.preventDefault();
  closeRecord();
});
drawer.addEventListener('keydown', event => {
  if (event.key !== 'Tab') return;
  const controls = [...drawer.querySelectorAll('a[href], button:not([disabled]), [tabindex="0"]')]
    .filter(control => control.getClientRects().length > 0);
  const first = controls[0];
  const last = controls[controls.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});
let backdropPressed = false;
drawer.addEventListener('pointerdown', event => {
  backdropPressed = event.target === drawer;
});
drawer.addEventListener('click', event => {
  if (backdropPressed && event.target === drawer) closeRecord();
  backdropPressed = false;
});
drawer.addEventListener('close', finishRecord);
for (const details of document.querySelectorAll('.record-details')) {
  details.addEventListener('toggle', () => {
    details.querySelector('summary').textContent = details.open ? '收起详情' : '查看详情';
  });
}
for (const link of document.querySelectorAll('a[href^="#"]:not(.citation-link):not(.citation-group-link)')) {
  link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    revealRecordTarget(target);
    const details = target?.closest('details');
    if (details) details.open = true;
    if (drawer.open && target && !drawer.contains(target)) closeRecord();
    const navMenu = link.closest('.nav-details');
    if (navMenu) navMenu.open = false;
  });
}
function revealHashTarget() {
  const target = document.getElementById(location.hash.slice(1));
  if (!target?.closest('article.record')) return;
  revealRecordTarget(target);
  requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
}
revealHashTarget();
window.addEventListener('hashchange', revealHashTarget);
for (const details of document.querySelectorAll('.nav-details')) {
  details.addEventListener('toggle', () => {
    if (!details.open) return;
    for (const other of document.querySelectorAll('.nav-details[open]')) {
      if (other !== details) other.open = false;
    }
    const menu = details.querySelector('.nav-menu');
    const bounds = details.getBoundingClientRect();
    const width = Math.min(320, innerWidth - 32);
    menu.style.width = width + 'px';
    menu.style.left = Math.max(16, Math.min(bounds.left, innerWidth - width - 16)) + 'px';
    const below = innerHeight - bounds.bottom - 24;
    const above = bounds.top - 24;
    const height = Math.min(menu.scrollHeight, 420, Math.max(below, above));
    menu.style.maxHeight = Math.max(80, height) + 'px';
    menu.style.top = below >= height ? bounds.bottom + 8 + 'px' : Math.max(16, bounds.top - height - 8) + 'px';
  });
}
document.addEventListener('pointerdown', event => {
  for (const details of document.querySelectorAll('.nav-details[open]')) {
    if (!details.contains(event.target)) details.open = false;
  }
});
const navigationSize = new ResizeObserver(entries => {
  root.style.setProperty('--chapter-bar-height', entries[0].contentRect.height + 'px');
});
navigationSize.observe(document.querySelector('.chapter-bar'));
const chapterLinks = [...document.querySelectorAll('.chapter-link')];
const sectionObserver = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    for (const link of chapterLinks) {
      if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
}, { rootMargin: '-5% 0px -70% 0px' });
for (const section of document.querySelectorAll('main > section')) sectionObserver.observe(section);
let printDetails = [];
let printRecordGroups = null;
window.addEventListener('beforeprint', () => {
  if (printRecordGroups === null) printRecordGroups = [...recordGroups.values()].map(state => [state, state.visibleCount, state.matchingCards, state.enabled]);
  for (const [state] of printRecordGroups) {
    state.matchingCards = state.cards;
    state.enabled = true;
    updateRecordGroup(state, state.cards.length);
  }
  hideImagePreview();
  restoreRecordSource();
  printDetails = [...document.querySelectorAll('.record-details:not([open]), .history-records:not([open])')];
  for (const details of printDetails) details.open = true;
});
window.addEventListener('afterprint', () => {
  for (const details of printDetails) details.open = false;
  printDetails = [];
  if (drawer.open && activeRecord) drawerBody.append(activeRecord.source);
  if (printRecordGroups !== null) {
    for (const [state, count, matches, enabled] of printRecordGroups) {
      state.matchingCards = matches;
      state.enabled = enabled;
      updateRecordGroup(state, count);
    }
    printRecordGroups = null;
  }
});
