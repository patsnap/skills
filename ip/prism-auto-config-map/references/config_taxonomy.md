# Configuration And Product-Domain Taxonomy

Normalize user prompts into product domains before detailed configuration analysis. If the user names a product domain, the report must first show:

`产品域 → 一级技术 → 二级配置/零部件 → 供应商类型 → 竞品/专利/供应链分析对象`

## Product Domains

| Product Domain | Level-1 Technologies | Typical Configurations / Components | Supplier Types |
|---|---|---|---|
| smart_cockpit / 智能座舱 | cockpit OS, HMI, display, voice/AI assistant, cockpit domain controller | screen layout, passenger screen, HUD/AR-HUD, app ecosystem, multimodal interaction, rear control, cabin chip | OEM, Tier0 ecosystem integrator, Tier1 cockpit electronics, Tier2 display/chip/module |
| intelligent_chassis / 智能底盘 | suspension control, braking, steering, body control, motion control | air suspension, CDC damping, rear-wheel steering, brake-by-wire, steer-by-wire, active anti-roll | OEM, Tier1 chassis system, Tier2 actuator/sensor/controller |
| adas_safety / 智驾与安全 | perception, decision, control, parking, occupant safety | LiDAR, radar/camera sensors, high-speed NOA, urban NOA, automated parking, AEB, DMS, child presence detection | OEM, Tier0 intelligent driving integrator, Tier1 sensor/ADAS, Tier2 chips/algorithms |
| thermal_management / 热管理 | cabin thermal comfort, battery thermal, heat pump, local heating | heating floor, seat heating/ventilation, multi-zone climate, heat pump, battery cooling/heating, thermal controller | Tier1 thermal system, Tier2 compressor/valve/heating film/material |
| battery_e_drive / 电池电驱 | cell, pack, BMS, motor, inverter, thermal safety | blade battery, solid-state battery signal, CTB/CTC, SiC inverter, e-axle, fast charging | OEM, battery supplier, e-drive Tier1, power electronics Tier2 |
| seat_comfort / 座椅舒适 | seat structure, actuation, sensing, heating/ventilation, storage | second-row leg rest, zero-gravity seat, seat drawer, second-row table, massage, boss key | Tier1 seat system, Tier2 motor/rail/frame/sensor/heating material |
| exterior_body_electronics / 外饰车身电子 | body access, mirror/vision, lighting, roof/body utility | electronic exterior mirror, hidden door handle, light signature, panoramic roof, roof rack | Tier1 body electronics, Tier2 camera/display/lighting/actuator |

## Stable Configuration Buckets

Use these stable categories in output data:

- `smart_cockpit`
- `intelligent_chassis`
- `adas_safety`
- `thermal_management`
- `battery_e_drive`
- `seat_comfort`
- `exterior_body_electronics`
- `interior_hmi`
- `exterior_design`

When a configuration belongs to multiple categories, choose the category that matches the user's decision question and state the secondary category in notes.

## Pain-Point Levels For QFD

| Level | Meaning | Example Signal |
|---|---|---|
| P0 critical | strongly affects safety, regulation, purchase rejection, or core experience | safety complaints, regulation, severe missing baseline |
| P1 high | frequently affects target persona satisfaction or major buying reason | family comfort, cold-weather energy/comfort, cockpit usability |
| P2 medium | adds visible value but is not decisive alone | convenience, trim differentiation, moderate comfort improvement |
| P3 low | nice-to-have or niche value | styling preference, occasional-use feature |

## Legacy Configuration Names

### Seat And Comfort

- front seat ventilation/heating/massage
- second-row leg rest
- second-row table
- boss key
- zero-gravity seat
- seat drawer/storage
- rear entertainment screen
- heating floor / cabin warm floor
- multi-zone climate comfort

### Interior And HMI

- screen size and layout
- passenger screen
- HUD / AR-HUD
- ambient light
- physical buttons vs touch controls
- center console layout
- materials: leather, suede, recycled materials, wood/metal trim
- voice assistant
- multimodal interaction

### Exterior And Styling

- electronic exterior mirror
- hidden door handle
- light signature
- wheel design
- roof rack / luggage compatibility
- color and trim package
- panoramic roof

### ADAS And Safety-Related Features

- LiDAR
- radar/camera sensor count
- high-speed NOA
- urban NOA
- automated parking
- AEB performance
- driver monitoring
- child presence detection
