(() => {
  'use strict';
  for (const controls of document.querySelectorAll('[data-record-browser]')) {
    const section = controls.closest('section');
    const buttons = [...controls.querySelectorAll('[data-filter-group]')];
    const status = controls.querySelector('[data-filter-status]');
    const empty = section.querySelector('[data-filter-empty]');
    const states = [...section.querySelectorAll('[data-record-group]')].map(list => recordGroups.get(list));
    if (states.some(state => !state) || !status || !empty) throw new Error('技术资料筛选缺少配置或目录');
    const total = new Set(states.flatMap(state => state.cards.map(card => card.dataset.recordKey))).size;
    let active = 'all';
    function applyFilters() {
      const matchingKeys = new Set();
      for (const state of states) {
        const wrapper = state.list.closest('[data-report-group]');
        state.enabled = active === 'all' || wrapper.dataset.reportGroup === active;
        state.matchingCards = state.cards;
        if (state.enabled) for (const card of state.matchingCards) matchingKeys.add(card.dataset.recordKey);
        wrapper.hidden = !state.enabled || state.matchingCards.length === 0;
        updateRecordGroup(state, state.initial);
      }
      for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filterGroup === active));
      status.textContent = '全部 ' + total + ' 条，当前目录 ' + matchingKeys.size + ' 条';
      empty.hidden = matchingKeys.size > 0;
      controls.dataset.matchingCount = String(matchingKeys.size);
      updateReadingProgress();
    }
    function resetFilters() {
      active = 'all';
      applyFilters();
    }
    for (const state of states) state.resetFilters = resetFilters;
    for (const button of buttons) button.addEventListener('click', () => {
      active = button.dataset.filterGroup;
      applyFilters();
    });
    applyFilters();
  }
  revealHashTarget();
})();
