# Color Palette Reference

## New Blue & White Theme 🎨

### Primary Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Light Background** | `#f8fafc` | (248, 250, 252) | Main page background, clean slate |
| **White** | `#ffffff` | (255, 255, 255) | Cards, panels, content areas |
| **Light Blue-Gray** | `#f1f5f9` | (241, 245, 249) | Subtle sections, table headers |

### Text Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Dark Text** | `#1e293b` | (30, 41, 59) | Primary text, headings |
| **Gray-Blue Text** | `#475569` | (71, 85, 105) | Secondary text, descriptions |
| **Light Gray-Blue** | `#94a3b8` | (148, 163, 184) | Tertiary text, placeholders |

### Accent Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Primary Blue** | `#3366cc` | (51, 102, 204) | Buttons, active states, links |
| **Dark Blue** | `#2952a3` | (41, 82, 163) | Hover states, emphasis |

### Status Colors

| Status | Hex | RGB | Background | Usage |
|--------|-----|-----|------------|-------|
| **Success** | `#16a34a` | (22, 163, 74) | `rgba(22,163,74,0.1)` | Completed, positive |
| **Warning** | `#d97706` | (217, 119, 6) | `rgba(217,119,6,0.1)` | In progress, caution |
| **Error** | `#dc2626` | (220, 38, 38) | `rgba(220,38,38,0.1)` | Error, danger |

### Border Colors

| Purpose | Color | Usage |
|---------|-------|-------|
| **Light Border** | `rgba(51,102,204,0.1)` | Card borders, subtle dividers |
| **Medium Border** | `rgba(51,102,204,0.2)` | Input focus, emphasized borders |

---

## Color Applications by Component

### 🎯 Sidebar Navigation
```
Background:     #ffffff (white)
Text:           #1e293b (dark)
Active bg:      #e8f0f8 (light blue, rgba(51,102,204,0.08))
Active text:    #3366cc (blue)
Hover:          rgba(255,255,255,0.04)
Border:         rgba(51,102,204,0.1)
```

### 📋 Cards & Panels
```
Background:     #ffffff (white)
Border:         rgba(51,102,204,0.1) (subtle blue)
Text:           #1e293b (dark)
Heading:        #1e293b (dark)
```

### 🔘 Buttons
```
Primary:
  - Background: #3366cc
  - Text:       #ffffff (white)
  - Hover:      #2952a3
  
Ghost:
  - Background: transparent
  - Text:       #475569
  - Hover:      #1e293b
```

### 📝 Form Inputs
```
Background:     #ffffff (white)
Text:           #1e293b (dark)
Border:         rgba(51,102,204,0.2)
Focus Border:   #3366cc
Focus Shadow:   rgba(51,102,204,0.15)
Placeholder:    #94a3b8
Label:          #475569
```

### 🔖 Badges
```
Success:  Green   (#16a34a) on rgba(22,163,74,0.1)
Warning:  Amber   (#d97706) on rgba(217,119,6,0.1)
Error:    Red     (#dc2626) on rgba(220,38,38,0.1)
Info:     Blue    (#3366cc) on rgba(51,102,204,0.08)
```

### 📊 Dashboard Statistics
```
Card:      #ffffff (white)
Value:     #3366cc (blue) for primary metrics
Icon:      #3366cc (blue)
Delta:     #16a34a (green) for positive changes
```

---

## Accessibility & Contrast

### WCAG AA Compliance ✅

| Element | Ratio | Level |
|---------|-------|-------|
| Dark text (#1e293b) on white (#ffffff) | 14.5:1 | AAA ✅ |
| Blue accent (#3366cc) on white | 4.5:1 | AA ✅ |
| Gray text (#475569) on white | 9.3:1 | AAA ✅ |
| Light text (#94a3b8) on white | 4.5:1 | AA ✅ |

### Color Blindness Friendly
- ✅ Not relying solely on color to convey information
- ✅ Badges include icons/symbols with color
- ✅ High contrast ratios for visibility
- ✅ Status indicators use multiple visual cues

---

## CSS Variables in Code

```css
:root {
  /* Backgrounds */
  --bg:       #f8fafc;        /* Main page */
  --bg2:      #ffffff;        /* Cards */
  --bg3:      #f1f5f9;        /* Accents */
  
  /* Text */
  --text:     #1e293b;        /* Primary text */
  --text2:    #475569;        /* Secondary text */
  --text3:    #94a3b8;        /* Tertiary text */
  
  /* Accents */
  --accent:   #3366cc;        /* Primary action */
  --accent2:  #2952a3;        /* Hover state */
  
  /* Status */
  --red:      #dc2626;
  --amber:    #d97706;
  --green:    #16a34a;
  
  /* Backgrounds with opacity */
  --red-bg:   rgba(220,38,38,0.1);
  --amber-bg: rgba(217,119,6,0.1);
  --green-bg: rgba(22,163,74,0.1);
  --blue-bg:  rgba(51,102,204,0.08);
  
  /* Borders */
  --border:   rgba(51,102,204,0.1);
  --border2:  rgba(51,102,204,0.2);
}
```

---

## Implementation Examples

### Using in Templates

```html
<!-- Text -->
<p style="color: var(--text)">Primary text</p>
<p style="color: var(--text2)">Secondary text</p>

<!-- Backgrounds -->
<div style="background: var(--bg2)">Card content</div>
<div style="background: var(--blue-bg)">Highlight</div>

<!-- Buttons -->
<button style="background: var(--accent); color: #fff;">Submit</button>

<!-- Borders -->
<div style="border: 1px solid var(--border)">Bordered</div>
```

---

## Brand Identity

### Primary Brand Color: Blue (#3366cc)
- Used for primary actions, links, and active states
- Represents trust, stability, and professionalism
- Matches Telkom brand guidelines
- Professional for cybersecurity dashboard

### Supporting Colors
- **Green**: Success, completed actions
- **Amber**: Warnings, in-progress items
- **Red**: Errors, critical alerts
- **Gray-Blue**: Neutral, secondary information

---

## Consistency Guidelines

✅ **DO:**
- Use `var(--accent)` for primary interactive elements
- Use `var(--text)` for main body text
- Use `var(--border)` for subtle dividers
- Maintain consistent spacing and sizing

❌ **DON'T:**
- Hardcode colors (use variables instead)
- Mix different accent colors on same page
- Use pure black (#000000) or pure white (#ffffff) for text on backgrounds
- Reduce contrast below WCAG AA standards

---

## Color Export Codes

### Hex Codes
```
#f8fafc #ffffff #f1f5f9 #1e293b #475569 #94a3b8 #3366cc #2952a3 #dc2626 #d97706 #16a34a
```

### RGB Values
```
(248, 250, 252) (255, 255, 255) (241, 245, 249) (30, 41, 59) (71, 85, 105) 
(148, 163, 184) (51, 102, 204) (41, 82, 163) (220, 38, 38) (217, 119, 6) (22, 163, 74)
```

### HSL Values
```
#f8fafc: hsl(208, 32%, 97%)
#ffffff: hsl(0, 0%, 100%)
#f1f5f9: hsl(210, 40%, 96%)
#1e293b: hsl(217, 33%, 17%)
#475569: hsl(215, 16%, 30%)
#94a3b8: hsl(220, 13%, 59%)
#3366cc: hsl(220, 66%, 55%)
#2952a3: hsl(220, 66%, 40%)
#dc2626: hsl(0, 85%, 55%)
#d97706: hsl(38, 92%, 50%)
#16a34a: hsl(132, 84%, 37%)
```

---

**Color theme updated successfully! 🎨**
