# Run90 Red Premium UI reference

This folder freezes the approved visual direction for the Run90 UI-only redesign.

Rules:
- Do not change ABT parsing/saving logic.
- Do not change IC/BCM/RKE/ABS block behavior.
- Do not change HEX/bit mutation logic or checkbox semantics.
- Do not change admin business logic.
- Visual layer only.

Palette:
- background: #080A0D
- panel: #14171C
- border: #2B2F36
- accent red: #CD141C
- glow red: #FF242D
- primary text: #EBEBEB
- muted text: #AAAEB5

Approved composition: Mazda header + gauge decoration, four module tabs, module info card, compact function rows, As-Built rows with red changed-character highlighting, Open/Save controls, creator panel, matching admin/about dialogs.

Binary reference images/assets are tracked separately under assets/ui_red_premium and should be treated as presentation resources only; functional widgets remain native/Kivy controls.
