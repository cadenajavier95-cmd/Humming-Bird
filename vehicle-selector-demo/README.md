Vehicle Selector Demo

Files:
- `index.html` — static demo page
- `script.js` — dependent dropdown logic and sample dataset
- `styles.css` — minimal styling

How to run:
1. Open `index.html` in your browser. In PowerShell from the project folder run:

```powershell
Start-Process .\index.html
```

2. Use the `Make` dropdown to pick a manufacturer, then select `Model`. `Vehicle Type` and `Subtier (Doors)` will populate automatically.

Customizing data:
- Edit the `vehicleData` object in `script.js` to add makes, models, types, and door options.
- To load data from an API, replace `populateMakes()` with a `fetch('/api/vehicles')` call and adapt the returned JSON shape.

Next steps (optional):
- Add a React/Vue component for integration into a frontend app.
- Persist selections or prefill from user data.
