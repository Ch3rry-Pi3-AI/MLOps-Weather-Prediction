# 🎨 `static/style.css` — Frontend Theme and Layout

This file defines the **visual style** for the **Weather Prediction Flask application**.
It provides a modern, accessible, and mobile-responsive design, ensuring a smooth user experience for both casual and technical users.

The stylesheet focuses on **clarity, consistency, and maintainability**, using CSS variables and grid layouts to achieve a balanced, card-based interface.

## 🧩 Purpose

This stylesheet manages the complete look and feel of the application’s `index.html` page, including:

* Global colour palette and typography
* Layout and responsive grid system
* Input form styling and buttons
* Informational cards and alerts
* Subtle background overlay for visual depth

It ensures a **consistent brand identity** and **clean hierarchy**, allowing users to focus on the task: predicting whether it will rain tomorrow.

## 📁 File Location

```
project_root/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── style.css           # This file
    └── img/
        └── app_background.jpg
```

## ⚙️ Core Design Principles

| Principle          | Description                                                        |
| :----------------- | :----------------------------------------------------------------- |
| **Simplicity**     | A minimal, card-based interface for clarity and quick interaction. |
| **Readability**    | Poppins font family and high-contrast text for legibility.         |
| **Consistency**    | Uses CSS variables for unified colours, spacing, and shadows.      |
| **Responsiveness** | Automatically adapts to mobile and desktop via grid layouts.       |
| **Accessibility**  | Semantic markup and sufficient contrast for visual comfort.        |

## 🧠 Theme Variables

All visual aspects are controlled via CSS custom properties defined in the `:root` selector.

| Variable               | Purpose                                      | Example Value                  |
| :--------------------- | :------------------------------------------- | :----------------------------- |
| `--bg-overlay-opacity` | Transparency of the background image overlay | `0.22`                         |
| `--card-bg`            | Container background colour                  | `#ffffff`                      |
| `--text`               | Primary text colour                          | `#2c3e50`                      |
| `--muted`              | Secondary text colour                        | `#5b6b7a`                      |
| `--brand`              | Primary accent (buttons, links)              | `#3498db`                      |
| `--brand-hover`        | Hover variant of accent                      | `#2980b9`                      |
| `--ok`                 | Success messages and prediction highlights   | `#27ae60`                      |
| `--error`              | Error alerts                                 | `#e74c3c`                      |
| `--shadow`             | Soft elevation shadow for cards              | `0 10px 24px rgba(0,0,0,0.08)` |

These variables can be easily adjusted to re-skin the entire app while maintaining consistency.

## 🧩 Key Components

| Section                    | Description                                                                             |
| :------------------------- | :-------------------------------------------------------------------------------------- |
| **Global & Reset**         | Defines universal sizing (`box-sizing: border-box`) and sets font and body background.  |
| **Background Overlay**     | Provides a fixed, semi-transparent image behind the content using `app_background.jpg`. |
| **Container**              | Main card layout centred on the page with rounded corners and drop shadow.              |
| **Header & Subtitle**      | Defines hierarchy for title and tagline; uses muted colour for secondary text.          |
| **Stats / Guidance Cards** | Two compact cards showing unit ranges and default inference behaviour.                  |
| **Form Layout**            | Grid-based structure for even alignment of input fields (two columns on desktop).       |
| **Inputs & Labels**        | Consistent padding, border radius, and accessible text size.                            |
| **Primary Button**         | Prominent “Predict Rain Tomorrow” button with hover and active effects.                 |
| **Alerts / Results**       | Styled cards for displaying error or prediction messages.                               |
| **Responsive Rules**       | Adjusts grid layouts for single-column flow below 820px width.                          |

## 📱 Responsive Behaviour

* **Desktop:** Two-column layout for forms and guidance cards (`grid-template-columns: repeat(2, 1fr)`).
* **Mobile / Tablet:** Automatically collapses to a single column below 820px screen width.
* **Fluid Width:** Container constrained to `min(980px, 95vw)` ensuring adaptability on all devices.

## 🧩 Example Visual Flow

```
[ Header: Title + Subtitle ]

[ Input Guidance Cards ]
  ├── Units & Ranges
  └── Smart Defaults

[ Form Fields ]
  ├── Location (dropdown)
  ├── Date
  ├── Min / Max Temp
  ├── Humidity, Wind Speed, Rainfall
  └── [ Predict Button ]

[ Result or Error Message ]
```

## 🪄 Interaction Highlights

* **Hover Feedback:** Buttons subtly darken when hovered.
* **Press Feedback:** Buttons slightly depress on click (`transform: translateY(1px)`).
* **Focus States:** Inputs have clear borders and adequate padding for accessibility.
* **Result Colours:** Green for success predictions, red for input errors.

## 💡 Customisation Tips

* To change the **accent colour**, edit `--brand` and `--brand-hover`.
* To make the **background image more visible**, lower `--bg-overlay-opacity`.
* To adjust **card elevation**, modify the `--shadow` property.
* For a warmer tone, consider adjusting `--card-bg` to a soft beige (e.g., `#fff9f3`).

## 🧾 Maintenance Notes

* All styles are self-contained and require no external frameworks.
* The file supports any modern browser that implements CSS Grid and custom properties (Chrome 49+, Firefox 31+, Edge 15+, Safari 9.1+).
* Avoid adding inline styles in `index.html` except for dynamic background injection — this maintains clarity and separation of concerns.

## ✅ In summary

`style.css` defines a **modular, theme-driven frontend design** that blends clarity, responsiveness, and accessibility.
It complements the Flask backend by delivering a professional and user-friendly interface for the **Weather Prediction** model.
