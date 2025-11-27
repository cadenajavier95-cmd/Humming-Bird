// modelsByMake will be loaded from `data/models.json` at runtime.
let makes = [];
let modelsByMake = {};

// DOM refs
const makeInput = document.getElementById('makeInput');
const makeSuggestions = document.getElementById('makeSuggestions');
const modelInput = document.getElementById('modelInput');
const modelSuggestions = document.getElementById('modelSuggestions');
const typeSelect = document.getElementById('typeSelect');
const doorsSelect = document.getElementById('doorsSelect');
const typeLabel = document.getElementById('typeLabel');
const doorsLabel = document.getElementById('doorsLabel');
const summary = document.getElementById('summary');

// Show Type and Doors sections only when both Make and Model are selected
// Hide Type if there's only one option (auto-selected)
function showTypeAndDoorsIfReady() {
  if (makeInput.value && modelInput.value) {
    // Only show Type section if there are multiple options to choose from
    if (typeSelect.options.length > 1) {
      typeLabel.style.display = 'block';
    } else {
      typeLabel.style.display = 'none';
    }
  } else {
    typeLabel.style.display = 'none';
  }
  if (makeInput.value && modelInput.value && doorsSelect.options.length > 1) {
    doorsLabel.style.display = 'block';
  } else {
    doorsLabel.style.display = 'none';
  }
}

// Fuzzy search helper - scores matches based on relevance
function fuzzyScore(text, searchTerm) {
  const t = searchTerm.toLowerCase();
  const txt = text.toLowerCase();
  
  // Exact match gets highest score
  if (txt === t) return 1000;
  
  // Starts with search term gets very high score
  if (txt.startsWith(t)) return 500;
  
  // Word boundary match (e.g., "Mercedes" matches "Mercedes-Benz")
  if (txt.includes(' ' + t) || txt.includes('-' + t)) return 300;
  
  // Contains search term
  if (txt.includes(t)) {
    const pos = txt.indexOf(t);
    return 100 - pos; // Earlier matches score higher
  }
  
  // Levenshtein-like: character sequence match (e.g., "mrcds" matches "Mercedes")
  let charIndex = 0;
  for (let i = 0; i < txt.length && charIndex < t.length; i++) {
    if (txt[i] === t[charIndex]) charIndex++;
  }
  if (charIndex === t.length) return 50 - (t.length - charIndex);
  
  return 0; // No match
}

// Filter and show make suggestions with better ranking
function filterMakeSuggestions(term) {
  if (!term || !term.trim()) {
    makeSuggestions.style.display = 'none';
    makeSuggestions.innerHTML = '';
    return;
  }
  
  const t = term.trim();
  const scored = makes
    .map(m => ({ make: m, score: fuzzyScore(m, t) }))
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 12);
  
  if (!scored.length) {
    makeSuggestions.style.display = 'none';
    makeSuggestions.innerHTML = '';
    return;
  }
  
  makeSuggestions.innerHTML = scored.map(item => 
    `<div class="msugg" data-make="${item.make}" style="padding:8px 10px;cursor:pointer;border-bottom:1px solid #eee;hover:background:#f0f0f0;">${item.make}</div>`
  ).join('');
  makeSuggestions.style.display = 'block';
}

// Filter and show model suggestions with better ranking
function filterModelSuggestions(make, term) {
  modelSuggestions.style.display = 'none';
  modelSuggestions.innerHTML = '';
  if (!make || !term || !term.trim()) {
    return;
  }
  
  const t = term.trim();
  const models = modelsByMake[make] || [];
  const scored = models
    .map(m => ({ model: m, score: fuzzyScore(m.name, t) }))
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 20);
  
  if (!scored.length) {
    return;
  }
  
  modelSuggestions.innerHTML = scored.map(item => {
    const m = item.model;
    return `<div class="mmsugg" data-name="${m.name}" data-type="${m.type}" data-subtiers="${m.subtiers.join(',')}" style="padding:8px 10px;cursor:pointer;border-bottom:1px solid #eee;">${m.name} <span style="color:#666;font-size:12px;">— ${m.type}</span></div>`;
  }).join('');
  modelSuggestions.style.display = 'block';
}

// Helpers to check if there are suggestion matches (used for validation)
function hasMakeMatches(term) {
  if (!term || !term.trim()) return false;
  const t = term.trim().toLowerCase();
  // Accept if any make starts with the typed text (strong prefix match)
  if (makes.some(m => m.toLowerCase().startsWith(t))) return true;
  // Otherwise allow fuzzy suggestions only when the first character matches
  const first = t[0];
  return makes.some(m => m[0] && m[0].toLowerCase() === first && fuzzyScore(m, t) > 0);
}

function hasModelMatches(make, term) {
  if (!make || !term || !term.trim()) return false;
  const t = term.trim().toLowerCase();
  const models = modelsByMake[make] || [];
  // Prefer prefix matches first
  if (models.some(m => m.name.toLowerCase().startsWith(t))) return true;
  // Otherwise allow fuzzy matches only when the first character matches
  const first = t[0];
  return models.some(m => m.name[0] && m.name[0].toLowerCase() === first && fuzzyScore(m.name, t) > 0);
}

// On blur: don't allow values that have no suggestions
makeInput.addEventListener('blur', e => {
  const v = e.target.value.trim();
  if (!v) {
    makeSuggestions.style.display = 'none';
    return;
  }

  if (!hasMakeMatches(v)) {
    // invalid: clear and reset downstream fields
    e.target.value = '';
    makeSuggestions.style.display = 'none';
    modelInput.value = '';
    modelInput.disabled = true;
    modelSuggestions.style.display = 'none';
    typeSelect.innerHTML = '<option value="">— Select Type —</option>';
    typeSelect.disabled = true;
    doorsSelect.innerHTML = '<option value="">— Select Doors —</option>';
    doorsSelect.disabled = true;
    typeLabel.style.display = 'none';
    doorsLabel.style.display = 'none';

    const prev = e.target.placeholder;
    e.target.placeholder = 'Choose a make from suggestions';
    e.target.style.borderColor = 'crimson';
    setTimeout(() => { e.target.placeholder = prev; e.target.style.borderColor = ''; }, 1400);
    return;
  }

  // If the user typed an exact make name, enable models
  const exact = makes.find(m => m.toLowerCase() === v.toLowerCase());
  if (exact) {
    modelInput.disabled = false;
  }
});

modelInput.addEventListener('blur', e => {
  const v = e.target.value.trim();
  const make = makeInput.value;
  if (!v) {
    modelSuggestions.style.display = 'none';
    return;
  }

  if (!hasModelMatches(make, v)) {
    // invalid model for selected make: clear and reset downstream
    e.target.value = '';
    modelSuggestions.style.display = 'none';
    typeSelect.innerHTML = '<option value="">— Select Type —</option>';
    typeSelect.disabled = true;
    doorsSelect.innerHTML = '<option value="">— Select Doors —</option>';
    doorsSelect.disabled = true;
    typeLabel.style.display = 'none';
    doorsLabel.style.display = 'none';

    const prev = e.target.placeholder;
    e.target.placeholder = 'Choose a model from suggestions';
    e.target.style.borderColor = 'crimson';
    setTimeout(() => { e.target.placeholder = prev; e.target.style.borderColor = ''; }, 1400);
    return;
  }

  // If exact model name, populate type/subtiers automatically
  const models = modelsByMake[make] || [];
  const match = models.find(m => m.name.toLowerCase() === v.toLowerCase());
  if (match) {
    typeSelect.innerHTML = `<option value="${match.type}">${match.type}</option>`;
    typeSelect.value = match.type;
    typeSelect.disabled = false;
    doorsSelect.innerHTML = match.subtiers.map(s => `<option value="${s}">${s}</option>`).join('');
    if (doorsSelect.options.length > 0) {
      doorsSelect.options[0].selected = true;
      doorsSelect.disabled = false;
    } else {
      doorsSelect.disabled = true;
    }
    showTypeAndDoorsIfReady();
  }
});

// Update summary display
function updateSummary() {
  const make = makeInput.value;
  const model = modelInput.value || '';
  const type = typeSelect.value;
  const doors = doorsSelect.value;
  if (!make) { 
    summary.textContent = 'No selection yet.'; 
    return; 
  }
  summary.textContent = `${make} ${model || ''}${type ? ' — ' + type : ''}${doors ? ' — ' + doors : ''}`;
}

// Event: Make input changed
makeInput.addEventListener('input', e => {
  filterMakeSuggestions(e.target.value);
  // Reset downstream
  modelInput.value = '';
  modelInput.disabled = true;
  modelSuggestions.style.display = 'none';
  typeSelect.innerHTML = '<option value="">— Select Type —</option>';
  typeSelect.disabled = true;
  doorsSelect.innerHTML = '<option value="">— Select Doors —</option>';
  doorsSelect.disabled = true;
  typeLabel.style.display = 'none';
  doorsLabel.style.display = 'none';
  updateSummary();
});

// Event: Make suggestion clicked
makeSuggestions.addEventListener('click', e => {
  const item = e.target.closest('.msugg');
  if (!item) return;
  const make = item.getAttribute('data-make');
  makeInput.value = make;
  makeSuggestions.style.display = 'none';
  modelInput.disabled = false;
  modelInput.focus();
  updateSummary();
});

// Event: Model input changed
modelInput.addEventListener('input', e => {
  const make = makeInput.value;
  if (!make) return;
  filterModelSuggestions(make, e.target.value);
  updateSummary();
});

// Event: Model suggestion clicked
modelSuggestions.addEventListener('click', e => {
  const item = e.target.closest('.mmsugg');
  if (!item) return;
  const name = item.getAttribute('data-name');
  const type = item.getAttribute('data-type');
  const subtiers = (item.getAttribute('data-subtiers') || '').split(',').filter(Boolean);
  modelInput.value = name;
  modelSuggestions.style.display = 'none';
  // Populate vehicle type
  typeSelect.innerHTML = `<option value="${type}">${type}</option>`;
  typeSelect.value = type;
  typeSelect.disabled = false;
  // Populate subtiers (doors/cab type/etc) — only enable if there are options
  doorsSelect.innerHTML = subtiers.map(s => `<option value="${s}">${s}</option>`).join('');
  if (doorsSelect.options.length > 0) {
    doorsSelect.options[0].selected = true;
    doorsSelect.disabled = false;
  } else {
    doorsSelect.disabled = true;
  }
  showTypeAndDoorsIfReady();
  updateSummary();
});

// Event: Type select changed
typeSelect.addEventListener('change', updateSummary);

// Event: Doors select changed
doorsSelect.addEventListener('change', updateSummary);

console.log('Vehicle selector initialized. Makes:', makes.length, 'available.');

// Load models data and initialize makes/models
fetch('data/models.json')
  .then(r => r.json())
  .then(data => {
    modelsByMake = data;
    makes = Object.keys(modelsByMake).sort();
    console.log('Loaded models.json — makes available:', makes.length);
  })
  .catch(err => {
    console.error('Failed to load data/models.json', err);
  });
