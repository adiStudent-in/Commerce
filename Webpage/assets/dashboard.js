'use strict';

const PAGE = document.body.dataset.page || 'home';
const isNotesPage = PAGE === 'notes';

/* ─── Icons ─── */

const ICONS = {
  bst: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V11M10 20V5M16 20v-6M21 20V8"/><path d="M2.5 20h19"/></svg>',
  eco: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M8.8 7.8h6.4M8.8 10.7h6.4M13.2 8c2.1 0 2.7 2.7 0 2.7H8.8l4.8 4.9"/></svg>',
  stats: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 3.5v17h16"/><path d="M7.5 16.5v-5M11.5 16.5v-9M15.5 16.5v-6.5M19.5 16.5v-11"/></svg>',
  retail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.2 8h13.6l1 12H4.2l1-12Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg>',
  english: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 6.4C10.4 4.9 8.3 4.4 4.3 4.4v13c4 0 6.1.5 7.7 2 1.6-1.5 3.7-2 7.7-2v-13c-4 0-6.1.5-7.7 2Z"/><path d="M12 6.4v13"/></svg>',
  maths: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 20 12 4l8.5 16h-17Z"/><path d="M7.6 20 12 11.5 16.4 20"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4.5 12.5 4.5 4.5L20 6.6"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
  pencil: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h4.2L19 9.2 14.8 5 4 15.8V20Z"/><path d="m13.6 6.2 4.2 4.2"/></svg>'
};

const icon = (name) => ICONS[name] || ICONS.bst;

/* ─── Library data ─── */

const SUBJECTS = [
  { key: 'bst', name: 'Business Studies', short: 'BST', icon: 'bst', desc: 'NCERT · 10 chapters · notes + quick revision' },
  { key: 'eco', name: 'Micro-Economics', short: 'ECO', icon: 'eco', desc: 'Introductory micro · 11 complete notes' },
  { key: 'stats', name: 'Statistics', short: 'STAT', icon: 'stats', desc: 'Statistics for Economics · 6 chapters' },
  { key: 'retail', name: 'Retail', short: 'RET', icon: 'retail', desc: 'Vocational · 5 units · 20 sessions' },
  { key: 'english', name: 'English', short: 'ENG', icon: 'english', desc: 'Hornbill · Snapshots · 5 poems' },
  { key: 'maths', name: 'Mathematics', short: 'MATH', icon: 'maths', desc: 'Chapters 7–9 · master notes + easy revision' }
];

const GROUPS = [
  { name: 'Business Studies', key: 'bst', icon: 'bst' },
  { name: 'Micro-Economics', key: 'eco', icon: 'eco' },
  { name: 'Statistics', key: 'stats', icon: 'stats' },
  { name: 'Retail', key: 'retail', icon: 'retail' },
  { name: 'English · Hornbill', key: 'english', icon: 'english' },
  { name: 'English · Snapshots', key: 'english', icon: 'english' },
  { name: 'English · Poems', key: 'english', icon: 'english' },
  { name: 'Mathematics', key: 'maths', icon: 'maths' }
];

const DATA = [
  { key: 'bst', group: 'Business Studies', num: '1', id: 'bst-1', title: 'Business, Trade and Commerce', meta: 'Economy, industry, trade & commerce', file: 'BST/Chapter-1-Business-Trade-and-Commerce.html' },
  { key: 'bst', group: 'Business Studies', num: '2', id: 'bst-2', title: 'Forms of Business Organisation', meta: 'Sole proprietorship, HUF, partnership, cooperative & company', file: 'BST/Chapter-2-Forms-of-Business-Organisation.html' },
  { key: 'bst', group: 'Business Studies', num: '3', id: 'bst-3', title: 'Private, Public & Global Enterprises', meta: 'Public sector forms, global enterprises, joint ventures & PPP', file: 'BST/Chapter-3-Private-Public-and-Global-Enterprise.html' },
  { key: 'bst', group: 'Business Studies', num: '4', id: 'bst-4', title: 'Business Services', meta: 'Banking, insurance, communication & warehousing', file: 'BST/Chapter-4-Business-Services.html' },
  { key: 'bst', group: 'Business Studies', num: '5', id: 'bst-5', title: 'Emerging Modes of Business', meta: 'e-Business, its four branches & outsourcing', file: 'BST/Chapter-5-Emerging-Modes-of-Business.html' },
  { key: 'bst', group: 'Business Studies', num: '6', id: 'bst-6', title: 'Social Responsibilities & Business Ethics', meta: 'Interest groups, pollution & ethics', file: 'BST/Chapter-6-Social-Responsibilities-and-Business-Ethics.html' },
  { key: 'bst', group: 'Business Studies', num: '7', id: 'bst-7', title: 'Sources of Business Finance', meta: 'Shares, debentures, trade credit & deposits', file: 'BST/Chapter-7-Sources-of-Business-Finance.html' },
  { key: 'bst', group: 'Business Studies', num: '8', id: 'bst-8', title: 'Small Business and Enterprises', meta: 'Entrepreneurship, MSME, startups & IPR', file: 'BST/Chapter-8-Small-Business-and-Enterprises.html' },
  { key: 'bst', group: 'Business Studies', num: '9', id: 'bst-9', title: 'Internal Trade', meta: 'Wholesale, retail, mail order & GST', file: 'BST/Chapter-9-Internal-Trade.html' },
  { key: 'bst', group: 'Business Studies', num: '10', id: 'bst-10', title: 'International Business', meta: 'Trade types, entry modes, export–import & WTO', file: 'BST/Chapter-10-International-Business.html' },

  { key: 'eco', group: 'Micro-Economics', num: '1', id: 'econ-1', title: 'Introduction to Microeconomics — Complete Notes', meta: 'Scarcity, opportunity cost & the PPF, micro vs macro & positive vs normative', file: 'Economics/Chapter-1-Introduction-to-Microeconomics.html' },
  { key: 'eco', group: 'Micro-Economics', num: '2', id: 'econ-2', title: "Consumer's Equilibrium — Complete Notes", meta: 'Utility, TU–MU, indifference curves, budget line & tangency', file: 'Economics/Chapter-2-Consumer-Equilibrium.html' },
  { key: 'eco', group: 'Micro-Economics', num: '3', id: 'econ-3', title: 'Demand — Complete Notes', meta: 'Meaning, law of demand, shifts, market demand & exceptions', file: 'Economics/Chapter-3-Demand.html' },
  { key: 'eco', group: 'Micro-Economics', num: '4', id: 'econ-4', title: 'Elasticity of Demand — Complete Notes', meta: 'Percentage method, five degrees, TE & geometric methods, determinants', file: 'Economics/Chapter-4-Elasticity-of-Demand.html' },
  { key: 'eco', group: 'Micro-Economics', num: '5', id: 'econ-5', title: 'Production Function — Complete Notes', meta: 'Production function, TP, AP, MP, stages & returns to scale', file: 'Economics/Chapter-5-Production-Function.html' },
  { key: 'eco', group: 'Micro-Economics', num: '6', id: 'econ-6', title: 'Cost — Complete Notes', meta: 'TFC, TVC, TC, AFC, AVC, AC & MC', file: 'Economics/Chapter-6-Cost.html' },
  { key: 'eco', group: 'Micro-Economics', num: '7', id: 'econ-7', title: 'Revenue — Complete Notes', meta: 'TR, AR, MR, perfect vs imperfect competition & elasticity', file: 'Economics/Chapter-7-Revenue.html' },
  { key: 'eco', group: 'Micro-Economics', num: '8', id: 'econ-8', title: "Producer's Equilibrium — Complete Notes", meta: 'TR–TC, MR–MC, profit cases & shutdown', file: 'Economics/Chapter-8-Producer-Equilibrium.html' },
  { key: 'eco', group: 'Micro-Economics', num: '9', id: 'econ-9', title: 'Supply — Complete Notes', meta: 'Stock vs supply, law of supply, movement vs shift', file: 'Economics/Chapter-9-Supply.html' },
  { key: 'eco', group: 'Micro-Economics', num: '10', id: 'econ-10', title: 'Main Market Forms — Complete Notes', meta: 'Perfect competition, monopoly, monopolistic competition & oligopoly', file: 'Economics/Chapter-10-Main-Market-Forms.html' },
  { key: 'eco', group: 'Micro-Economics', num: '11', id: 'econ-11', title: 'Price Determination — Complete Notes', meta: 'Equilibrium, shifts, price ceiling & floor', file: 'Economics/Chapter-11-Price-Determination.html' },

  { key: 'stats', group: 'Statistics', num: '1', id: 'stat-1', title: 'Economics — An Introduction', meta: 'Definitions, scarcity, activities & more', file: 'Statistics/Chapter-1-Introduction-to-Economics.html' },
  { key: 'stats', group: 'Statistics', num: '2', id: 'stat-2', title: 'Meaning, Scope & Importance of Statistics', meta: 'Plural vs singular, functions, limitations', file: 'Statistics/Chapter-2-Meaning-Scope-and-Importance-of-Statistics.html' },
  { key: 'stats', group: 'Statistics', num: '3', id: 'stat-3', title: 'Collection of Data', meta: 'Primary vs secondary, sampling & more', file: 'Statistics/Chapter-3-Collection-of-Data.html' },
  { key: 'stats', group: 'Statistics', num: '4', id: 'stat-4', title: 'Organisation of Data', meta: 'Classification, frequency distribution & more', file: 'Statistics/Chapter-4-Organisation-of-Data.html' },
  { key: 'stats', group: 'Statistics', num: '5', id: 'stat-5', title: 'Tabular Presentation', meta: 'Parts of a table, types of tables & more', file: 'Statistics/Chapter-5-Tabular-Presentation.html' },
  { key: 'stats', group: 'Statistics', num: '6', id: 'stat-6', title: 'Measures of Central Tendency — Mean', meta: 'Formulas, steps & 11 solved questions', file: 'Statistics/Chapter-6-Measures-of-Central-Tendency-Mean.html' },

  { key: 'retail', group: 'Retail', num: '1', title: 'Fundamentals of Retailing', meta: '4 sessions · key terms · 10 exam Q&A', file: 'Retail/Unit-1-Fundamentals-of-Retailing.html' },
  { key: 'retail', group: 'Retail', num: '2', title: 'Process of Credit Application', meta: '4 sessions · credit checks · Five Cs', file: 'Retail/Unit-2-Process-of-Credit-Application.html' },
  { key: 'retail', group: 'Retail', num: '3', title: 'Mechanism for Customers to Choose Right Products', meta: '4 sessions · selling methods · closing a sale', file: 'Retail/Unit-3-Mechanism-for-Customers-to-Choose-Right-Products.html' },
  { key: 'retail', group: 'Retail', num: '4', title: 'Specialist Support to Customers', meta: '4 sessions · personalisation · post-sales support', file: 'Retail/Unit-4-Specialist-Support-to-Customers.html' },
  { key: 'retail', group: 'Retail', num: '5', title: 'Health and Safety Management', meta: '4 sessions · risks · emergencies · reporting', file: 'Retail/Unit-5-Health-and-Safety-Management.html' },

  { key: 'english', group: 'English · Hornbill', num: '1', title: 'The Portrait of a Lady', meta: 'Khushwant Singh · summary, character sketch, 12 exam Q&A', file: 'English/Chapter-1-The-Portrait-of-a-Lady.html' },
  { key: 'english', group: 'English · Hornbill', num: '2', title: "We're Not Afraid to Die… if We Can All Be Together", meta: 'Gordon Cook & Alan East · true sea adventure', file: 'English/Chapter-2-Were-Not-Afraid-to-Die.html' },
  { key: 'english', group: 'English · Hornbill', num: '3', title: 'Discovering Tut: The Saga Continues', meta: 'A. R. Williams · archaeology & the CT scan', file: 'English/Chapter-3-Discovering-Tut.html' },
  { key: 'english', group: 'English · Hornbill', num: '4', title: "The Ailing Planet: the Green Movement's Role", meta: 'Nani Palkhivala · persuasive article', file: 'English/Chapter-4-The-Ailing-Planet.html' },
  { key: 'english', group: 'English · Hornbill', num: '5', title: 'The Adventure', meta: 'Jayant Narlikar · science fiction', file: 'English/Chapter-5-The-Adventure.html' },
  { key: 'english', group: 'English · Hornbill', num: '6', title: 'Silk Road', meta: 'Nick Middleton · travelogue, journey to Kailash', file: 'English/Chapter-6-Silk-Road.html' },

  { key: 'english', group: 'English · Snapshots', num: 'S1', title: 'The Summer of the Beautiful White Horse', meta: 'William Saroyan · tale of trust & honesty', file: 'English/Chapter-1-The-Summer-of-the-Beautiful-White-Horse.html' },
  { key: 'english', group: 'English · Snapshots', num: 'S2', title: 'The Address', meta: 'Marga Minco · post-War story, Holland', file: 'English/Chapter-2-The-Address.html' },
  { key: 'english', group: 'English · Snapshots', num: 'S3', title: "Mother's Day", meta: 'J.B. Priestley · one-act play', file: 'English/Chapter-3-Mothers-Day.html' },
  { key: 'english', group: 'English · Snapshots', num: 'S4', title: 'Birth', meta: 'A. J. Cronin · from The Citadel', file: 'English/Chapter-4-Birth.html' },
  { key: 'english', group: 'English · Snapshots', num: 'S5', title: 'The Tale of Melon City', meta: 'Vikram Seth · narrative comic poem', file: 'English/Chapter-5-The-Tale-of-Melon-City.html' },

  { key: 'english', group: 'English · Poems', num: 'P1', title: 'A Photograph', meta: 'Shirley Toulson · time, memory and loss', file: 'English/Poem-1-A-Photograph.html' },
  { key: 'english', group: 'English · Poems', num: 'P2', title: 'The Laburnum Top', meta: 'Ted Hughes · the goldfinch and the tree', file: 'English/Poem-2-The-Laburnum-Top.html' },
  { key: 'english', group: 'English · Poems', num: 'P3', title: 'The Voice of the Rain', meta: 'Walt Whitman · the water cycle as song', file: 'English/Poem-3-The-Voice-of-the-Rain.html' },
  { key: 'english', group: 'English · Poems', num: 'P4', title: 'Childhood', meta: 'Markus Natten · loss of innocence', file: 'English/Poem-4-Childhood.html' },
  { key: 'english', group: 'English · Poems', num: 'P5', title: 'Father to Son', meta: 'Elizabeth Jennings · the generation gap', file: 'English/Poem-5-Father-to-Son.html' },

  { key: 'maths', group: 'Mathematics', num: '7', title: 'Binomial Theorem — Easy Revision', meta: 'STE100 easy notes · 42 solved questions, Pascal’s triangle & formula wall', file: 'Maths/Chapter-7-Binomial-Theorem-STE100.html' },
  { key: 'maths', group: 'Mathematics', num: '8', title: 'Sequences and Series', meta: 'Concept-first master notes · GP, infinite GP, GM & AM–GM', file: 'Maths/Chapter-8-Sequences-and-Series.html' },
  { key: 'maths', group: 'Mathematics', num: '8', title: 'Sequences and Series — Easy Revision', meta: 'STE100 easy notes · 42 solved questions, formula wall & traps', file: 'Maths/Chapter-8-Sequences-and-Series-STE100.html' },
  { key: 'maths', group: 'Mathematics', num: '9', title: 'Straight Lines — Easy Revision', meta: 'STE100 easy notes · slopes, forms of a line & solved examples', file: 'Maths/Chapter-9-Straight-Lines-STE100.html' }
];

const DEFAULT_FOCUS = [
  { id: 'focus-bst', text: 'Revise BST Ch.1 — business vs profession vs employment', meta: 'Business Studies · Chapter 1', chapter: 'BST/Chapter-1-Business-Trade-and-Commerce.html' },
  { id: 'focus-eco', text: 'Micro Ch.2 — one diagram: TU and MU, or the budget line', meta: 'Micro-Economics · Chapter 2', chapter: 'Economics/Chapter-2-Consumer-Equilibrium.html' },
  { id: 'focus-eng', text: 'Read 10 pages — The Portrait of a Lady', meta: 'English · Hornbill · Chapter 1', chapter: 'English/Chapter-1-The-Portrait-of-a-Lady.html' }
];

const FOCUS_TASKS_KEY = 'studyos-focus-tasks-v1';
const MAX_FOCUS_TASKS = 6;
const TOTAL_NOTES = DATA.length;
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const now = new Date();
const todayKey = 'studyos-focus-' + now.toISOString().slice(0, 10);
const themeKey = 'study-os-theme';
const lastNoteKey = 'studyos-last-note';

let activeFilter = 'all';
let query = '';
let focusItems = loadFocusTasks();
let focusState = readJSON(todayKey) || {};
let editingFocusId = null;
let toastTimer = 0;
let lastFocused = null;

function readJSON(key) {
  try { return JSON.parse(localStorage.getItem(key)) || null; }
  catch (error) { return null; }
}

function writeJSON(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); }
  catch (error) { /* private mode */ }
}

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

/* ─── Continue reading (real last-opened note) ─── */

function findNote(file) {
  return DATA.find((item) => item.file === file) || null;
}

function subjectOf(item) {
  return SUBJECTS.find((subject) => subject.key === item.key) || SUBJECTS[0];
}

function saveLastNote(file) {
  const item = findNote(file);
  if (!item) return;
  const previous = readJSON(lastNoteKey);
  const visits = previous && previous.file === file ? (Number(previous.visits) || 1) + 1 : 1;
  writeJSON(lastNoteKey, { file, at: new Date().toISOString(), visits });
}

function lastNoteInfo() {
  const saved = readJSON(lastNoteKey);
  if (saved && saved.file) {
    const item = findNote(saved.file);
    if (item) {
      const at = saved.at ? new Date(saved.at) : null;
      return { item, at: at && !isNaN(at) ? at : null, visits: Number(saved.visits) || 1 };
    }
  }

  // Fall back to the shared chapter tracker used by the chapter pages.
  const progress = readJSON('study-os-progress') || {};
  let best = null;
  DATA.forEach((item) => {
    if (!item.id) return;
    const entry = progress[item.id];
    if (!entry || !entry.lastVisited) return;
    const stamp = Date.parse(entry.lastVisited);
    if (!Number.isFinite(stamp)) return;
    if (!best || stamp > best.stamp) {
      best = { item, stamp, visits: Number(entry.visitCount) || 1 };
    }
  });
  return best ? { item: best.item, at: new Date(best.stamp), visits: best.visits } : null;
}

function relativeTime(date) {
  if (!date) return '';
  const minutes = Math.max(0, Math.round((Date.now() - date.getTime()) / 60000));
  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
  const days = Math.round(hours / 24);
  if (days < 8) return `${days} ${days === 1 ? 'day' : 'days'} ago`;
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
}

function renderContinue() {
  const info = lastNoteInfo();
  const item = info ? info.item : DATA[0];
  const subject = subjectOf(item);
  const sameGroup = DATA.filter((entry) => entry.group === item.group);
  const isNumberedChapter = /^\d+$/.test(item.num);
  const kind = item.group.includes('Poems') ? 'Poem'
    : item.group.includes('Snapshots') ? 'Story'
      : item.group.includes('Retail') ? 'Unit'
        : isNumberedChapter ? 'Chapter' : 'Note';

  $('#continueCode').textContent = subject.short;
  $('#continueNum').textContent = String(item.num).padStart(2, '0');
  $('#continueOf').textContent = `of ${String(sameGroup.length).padStart(2, '0')}`;
  $('#continueSubject').textContent = `${item.group} · ${kind} ${item.num}`;
  $('#todayTitle').textContent = item.title;
  $('#continueDesc').textContent = item.meta;

  $('#continueLink').href = item.file;
  $('#continueLink').dataset.noteFile = item.file;
  $('#continueLink').firstChild.textContent = info ? 'Resume chapter ' : 'Open chapter ';

  const bar = $('#continueBar');
  if (info) {
    $('#continueLabel').textContent = 'Last opened';
    $('#continueNote').textContent = relativeTime(info.at);
    bar.style.width = '100%';
  } else {
    $('#continueLabel').textContent = 'Start here';
    $('#continueNote').textContent = `${subject.name} · ${subject.desc.split(' · ')[0]}`;
    bar.style.width = '0%';
  }
}

function renderUpNext() {
  const info = lastNoteInfo();
  const current = info ? info.item : DATA[0];
  const groupItems = DATA.filter((item) => item.group === current.group);
  const index = groupItems.indexOf(current);
  const ordered = [
    ...groupItems.slice(index + 1),
    ...DATA.filter((item) => item.group !== current.group)
  ].slice(0, 2);

  $('#upNextList').innerHTML = ordered.map((item) => `
    <a href="${item.file}" data-note-file="${item.file}">
      <span class="n">${item.num}</span>
      <span class="t">${item.title}</span>
      <span class="s">${item.group}</span>
    </a>`).join('');
}

/* ─── Study streak (from the shared chapter log) ─── */

function computeStreak() {
  const log = readJSON('study-os-study-log') || [];
  const days = new Set(log.filter((entry) => Number(entry.totalMinutes) > 0).map((entry) => entry.date));
  if (!days.size) return { current: 0, best: 0 };

  const cursor = new Date();
  if (!days.has(cursor.toISOString().slice(0, 10))) cursor.setDate(cursor.getDate() - 1);
  let current = 0;
  while (days.has(cursor.toISOString().slice(0, 10))) {
    current += 1;
    cursor.setDate(cursor.getDate() - 1);
  }

  const sorted = Array.from(days).sort();
  let best = 1;
  let run = 1;
  for (let i = 1; i < sorted.length; i += 1) {
    const previous = new Date(sorted[i - 1] + 'T00:00:00Z');
    const day = new Date(sorted[i] + 'T00:00:00Z');
    if (day - previous === 86400000) run += 1;
    else run = 1;
    if (run > best) best = run;
  }
  return { current, best };
}

function renderStreak() {
  const { current, best } = computeStreak();
  $('#streakDays').textContent = String(current);
  if (current === 0) {
    $('#streakNote').textContent = 'Open a chapter to start a streak.';
  } else if (best > current) {
    $('#streakNote').textContent = `Best run this term · ${best} days`;
  } else {
    $('#streakNote').textContent = 'Your best run yet — keep it going.';
  }
}

/* ─── Subject shelf ─── */

function renderSubjects() {
  const host = $('#subjectRows');
  host.innerHTML = SUBJECTS.map((subject) => {
    const items = DATA.filter((item) => item.key === subject.key);
    const latest = items[items.length - 1];
    return `<a class="subject-row" href="notes.html?subject=${subject.key}">
      <span class="subject-ic">${icon(subject.icon)}</span>
      <span class="subject-name"><b>${subject.name}</b><small>${subject.desc}</small></span>
      <span class="subject-latest"><span>Latest</span>${latest.title}</span>
      <span class="subject-count">${String(items.length).padStart(2, '0')}<small>notes</small></span>
      <span class="subject-arrow">${icon('arrow')}</span>
    </a>`;
  }).join('');
}

/* ─── Notes index ─── */

function renderFilters() {
  const filters = [
    { key: 'all', label: 'All', count: TOTAL_NOTES },
    ...SUBJECTS.map((subject) => ({
      key: subject.key,
      label: subject.name,
      count: DATA.filter((item) => item.key === subject.key).length
    }))
  ];

  $('#filterRow').innerHTML = filters.map((filter) => {
    const on = filter.key === activeFilter;
    return `<button class="chip${on ? ' on' : ''}" type="button" data-filter="${filter.key}" aria-pressed="${on}">
      ${filter.label}<span class="c">${filter.count}</span>
    </button>`;
  }).join('');
}

function paintFilters() {
  $$('#filterRow .chip').forEach((chip) => {
    const on = chip.dataset.filter === activeFilter;
    chip.classList.toggle('on', on);
    chip.setAttribute('aria-pressed', String(on));
  });
}

function setFilter(filter) {
  activeFilter = filter;
  paintFilters();
  renderNotes();
  updateNotesUrl();
}

function noteRow(item) {
  return `<a class="note-row" href="${item.file}" data-note-file="${item.file}">
    <span class="note-num">${item.num}</span>
    <span class="note-body">
      <span class="note-title">${item.title}</span>
      <span class="note-meta">${item.meta}</span>
    </span>
    <span class="note-arrow">${icon('arrow')}</span>
  </a>`;
}

function renderNotes() {
  const filtered = DATA.filter((item) => {
    if (activeFilter !== 'all' && item.key !== activeFilter) return false;
    if (!query) return true;
    const haystack = `${item.title} ${item.group} ${item.meta} ${item.num}`.toLowerCase();
    return haystack.includes(query);
  });

  const groups = GROUPS.map((group) => {
    const items = filtered.filter((item) => item.group === group.name);
    return { ...group, items };
  }).filter((group) => group.items.length);

  $('#notesList').innerHTML = groups.map((group) => `
    <section class="notes-group" aria-label="${group.name}">
      <div class="notes-group-head">
        <span class="g-ic" data-sub="${group.key}">${icon(group.icon)}</span>
        <h3>${group.name}</h3>
        <span class="g-count">${group.items.length} ${group.items.length === 1 ? 'note' : 'notes'}</span>
      </div>
      ${group.items.map(noteRow).join('')}
    </section>
  `).join('');

  const count = filtered.length;
  const queryLabel = $('#searchInput').value.trim();
  const countLabel = query
    ? `${count} ${count === 1 ? 'result' : 'results'} · “${queryLabel}”`
    : `${count} ${count === 1 ? 'note' : 'notes'}`;
  $('#notesCount').textContent = countLabel;

  const isEmpty = count === 0;
  $('#emptySearch').classList.toggle('show', isEmpty);
  $('#emptyQ').textContent = query ? queryLabel : 'that filter';
  if (isEmpty) $('#notesList').setAttribute('aria-hidden', 'true');
  else $('#notesList').removeAttribute('aria-hidden');
}

/* ─── Today's focus ─── */

const noteByFile = new Map(DATA.map((note) => [note.file, note]));

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]
  ));
}

function makeFocusId() {
  return 'focus-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7);
}

function loadFocusTasks() {
  const saved = readJSON(FOCUS_TASKS_KEY);
  if (!Array.isArray(saved)) return DEFAULT_FOCUS.map((task) => ({ ...task }));

  const seen = new Set();
  const tasks = [];

  saved.slice(0, MAX_FOCUS_TASKS).forEach((task) => {
    if (!task || typeof task !== 'object') return;
    const text = typeof task.text === 'string' ? task.text.trim().slice(0, 140) : '';
    if (!text) return;

    let id = typeof task.id === 'string' && /^[a-z0-9-]{1,80}$/i.test(task.id) ? task.id : makeFocusId();
    if (seen.has(id)) id = makeFocusId();
    seen.add(id);

    tasks.push({
      id,
      text,
      meta: typeof task.meta === 'string' ? task.meta.slice(0, 120) : '',
      chapter: typeof task.chapter === 'string' ? task.chapter : ''
    });
  });

  return tasks;
}

function saveFocusTasks() {
  writeJSON(FOCUS_TASKS_KEY, focusItems);
}

function focusMeta(note) {
  const unitWord = note.group === 'Retail' ? 'Unit' : 'Chapter';
  return `${note.group} · ${unitWord} ${note.num}`;
}

function populateFocusChapters() {
  const select = $('#focusChapter');
  const options = SUBJECTS.map((subject) => {
    const notes = DATA.filter((note) => note.key === subject.key);
    if (!notes.length) return '';

    const items = notes.map((note) => {
      const groupLabel = note.group === subject.name
        ? ''
        : note.group.replace(/^English · /, '') + ' · ';
      const label = `${groupLabel}${note.num}. ${note.title}`;
      return `<option value="${escapeHTML(note.file)}">${escapeHTML(label)}</option>`;
    }).join('');

    return `<optgroup label="${escapeHTML(subject.name)}">${items}</optgroup>`;
  }).join('');

  select.innerHTML = '<option value="">Custom to-do — no chapter</option>' + options;
}

function renderFocus() {
  const rows = focusItems.map((item) => {
    const done = Boolean(focusState[item.id]);
    const checkId = 'focus-check-' + item.id;
    const meta = item.meta ? `<span class="focus-meta">${escapeHTML(item.meta)}</span>` : '';
    return `<div class="focus-item${done ? ' done' : ''}">
      <input type="checkbox" id="${checkId}" data-focus="${escapeHTML(item.id)}"${done ? ' checked' : ''}>
      <label class="focus-box" for="${checkId}" aria-hidden="true">${icon('check')}</label>
      <label class="focus-txt" for="${checkId}">${escapeHTML(item.text)}${meta}</label>
      <button class="focus-edit" type="button" data-focus-edit="${escapeHTML(item.id)}" aria-label="Edit focus task" title="Edit task">${icon('pencil')}</button>
    </div>`;
  }).join('');

  $('#focusList').innerHTML = rows +
    `<button class="focus-add" type="button" data-focus-add>${icon('plus')} Add a chapter or to-do</button>`;
  updateFocus();
}

function updateFocus(announce = false) {
  const total = focusItems.length;
  const done = focusItems.filter((item) => focusState[item.id]).length;
  $('#focusCount').textContent = `${done} / ${total}`;

  const note = $('#focusNote');
  if (total === 0) note.textContent = 'No focus yet. Add a chapter or a small to-do.';
  else if (done === total) note.textContent = 'All done. Close the book.';
  else if (done === 0) note.textContent = 'Small wins. That’s the page.';
  else note.textContent = `${total - done} left. Small pages count.`;

  $('#focusReset').hidden = done === 0;

  if (announce && total > 0 && done === total) {
    showToast('All done — that’s today’s page.');
  }
}

function openFocusDialog(id = null) {
  const task = id ? focusItems.find((item) => item.id === id) : null;
  editingFocusId = task ? task.id : null;

  $('#focusDialogKicker').textContent = task ? 'Edit focus' : 'Today’s focus';
  $('#focusDialogTitle').textContent = task ? 'Edit this focus' : 'Add a focus';
  $('#focusDelete').hidden = !task;
  $('#focusChapter').value = task && task.chapter ? task.chapter : '';
  $('#focusText').value = task ? task.text : '';

  const dialog = $('#focusDialog');
  if (typeof dialog.showModal === 'function') dialog.showModal();
  else dialog.setAttribute('open', '');

  $('#focusText').focus();
  $('#focusText').select();
}

function closeFocusDialog() {
  const dialog = $('#focusDialog');
  if (typeof dialog.close === 'function') dialog.close();
  else dialog.removeAttribute('open');
  editingFocusId = null;
}

function submitFocusDialog() {
  const textInput = $('#focusText');
  const text = textInput.value.trim();
  if (!text) {
    textInput.focus();
    showToast('Write a small task first.');
    return;
  }

  const chapter = $('#focusChapter').value;
  const note = noteByFile.get(chapter);
  const meta = note ? focusMeta(note) : '';

  if (editingFocusId) {
    const task = focusItems.find((item) => item.id === editingFocusId);
    if (!task) return;
    task.text = text;
    task.chapter = chapter;
    task.meta = meta;
    showToast('Focus updated.');
  } else {
    if (focusItems.length >= MAX_FOCUS_TASKS) {
      showToast('Six focus tasks is plenty for one day.');
      return;
    }
    focusItems.push({ id: makeFocusId(), text, meta, chapter });
    showToast('Added to today’s focus.');
  }

  saveFocusTasks();
  renderFocus();
  closeFocusDialog();
}

function deleteFocusTask() {
  if (!editingFocusId) return;
  focusItems = focusItems.filter((item) => item.id !== editingFocusId);
  delete focusState[editingFocusId];
  saveFocusTasks();
  writeJSON(todayKey, focusState);
  renderFocus();
  closeFocusDialog();
  showToast('Focus removed.');
}

/* ─── Theme ─── */

const themeMeta = $('meta[name="theme-color"]');

function getSavedTheme() {
  try {
    const raw = localStorage.getItem(themeKey);
    if (raw === null) return null;
    try {
      const parsed = JSON.parse(raw);
      return parsed === 'dark' || parsed === 'light' ? parsed : null;
    } catch (parseError) {
      return raw === 'dark' || raw === 'light' ? raw : null;
    }
  } catch (error) {
    return null;
  }
}

function setTheme(theme, persist = true) {
  const isDark = theme === 'dark';
  document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
  if (themeMeta) themeMeta.setAttribute('content', isDark ? '#111310' : '#f4f0e6');

  const lightBtn = $('#lightBtn');
  const darkBtn = $('#darkBtn');
  if (lightBtn) {
    lightBtn.classList.toggle('on', !isDark);
    lightBtn.setAttribute('aria-pressed', String(!isDark));
  }
  if (darkBtn) {
    darkBtn.classList.toggle('on', isDark);
    darkBtn.setAttribute('aria-pressed', String(isDark));
  }

  if (persist) {
    // JSON matches how study-os.js stores its theme on chapter pages.
    try { localStorage.setItem(themeKey, JSON.stringify(isDark ? 'dark' : 'light')); }
    catch (error) { /* private mode */ }
  }
}

function toggleTheme() {
  setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
}

/* ─── Syllabus progress ─── */

function syncSyllabus() {
  const meta = readJSON('syllabus-tracker-meta');
  let pct = 34;
  let note = 'Preview — the tracker will sync here.';

  if (meta) {
    const done = Number(meta.done);
    const total = Number(meta.total);
    if (Number.isFinite(Number(meta.pct))) {
      pct = Math.max(0, Math.min(100, Math.round(Number(meta.pct))));
    } else if (Number.isFinite(done) && Number.isFinite(total) && total > 0) {
      pct = Math.round((done / total) * 100);
    }
    if (Number.isFinite(done) && Number.isFinite(total) && total > 0) {
      note = `${done} of ${total} topics checked.`;
    } else {
      note = 'Synced with your syllabus tracker.';
    }
  }

  $('#sidePct').textContent = `${pct}%`;
  $('#sideProgressNote').textContent = note;
  const ledgerPct = $('#ledgerPctNum');
  if (ledgerPct) ledgerPct.textContent = String(pct);
  const ledgerNote = $('#ledgerNote');
  if (ledgerNote) ledgerNote.textContent = meta ? 'Synced with your syllabus tracker.' : 'Preview · the tracker sets this.';
  $$('.progress[role="progressbar"]').forEach((bar) => bar.setAttribute('aria-valuenow', String(pct)));

  window.setTimeout(() => {
    $('#sideProgress').style.width = `${pct}%`;
    const ledgerBar = $('#ledgerBar');
    if (ledgerBar) ledgerBar.style.width = `${pct}%`;
  }, 140);
}

/* ─── Dates ─── */

function isoWeek(date) {
  const target = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const day = target.getUTCDay() || 7;
  target.setUTCDate(target.getUTCDate() + 4 - day);
  const yearStart = new Date(Date.UTC(target.getUTCFullYear(), 0, 1));
  return Math.ceil((((target - yearStart) / 86400000) + 1) / 7);
}

function setDates() {
  const hour = now.getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const weekday = now.toLocaleDateString('en-GB', { weekday: 'long' });
  const dateLong = now.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  const monthShort = now.toLocaleDateString('en-GB', { month: 'short' }).toUpperCase();

  $('#greetEyebrow').textContent = `${greeting} · ${dateLong}`;
  $('#dateDay').textContent = String(now.getDate());
  $('#dateMonth').textContent = monthShort;
  $('#dateWeek').textContent = `Week ${isoWeek(now)} · ${now.getFullYear()}`;
  $('#todayDate').textContent = weekday;
}

/* ─── Toast ─── */

function showToast(message) {
  const toast = $('#toast');
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('show'), 2600);
}

/* ─── Notes URL state ─── */

function updateNotesUrl() {
  if (!isNotesPage) return;
  const input = $('#searchInput');
  const params = new URLSearchParams();
  if (activeFilter !== 'all') params.set('subject', activeFilter);
  if (input && input.value.trim()) params.set('q', input.value.trim());
  const search = params.toString();
  history.replaceState(null, '', search ? `notes.html?${search}` : 'notes.html');
}

function readNotesUrl() {
  const input = $('#searchInput');
  const params = new URLSearchParams(window.location.search);
  const subject = params.get('subject');
  activeFilter = SUBJECTS.some((item) => item.key === subject) ? subject : 'all';

  const rawQuery = (params.get('q') || '').slice(0, 80);
  query = rawQuery.trim().toLowerCase();
  if (input) input.value = rawQuery;
}

/* ─── Drawer ─── */

const sidebar = $('#sidebar');
const scrim = $('#scrim');
const menuBtn = $('#menuBtn');
const mainEl = $('.main');

function openDrawer() {
  if (!sidebar || !scrim || !menuBtn || !mainEl) return;
  if (window.innerWidth > 900 || sidebar.classList.contains('open')) return;
  lastFocused = document.activeElement;
  sidebar.classList.add('open');
  scrim.classList.add('show');
  document.body.classList.add('nav-open');
  mainEl.inert = true;
  menuBtn.setAttribute('aria-expanded', 'true');
  window.setTimeout(() => {
    const first = $('.nav-item', sidebar);
    if (first) first.focus({ preventScroll: true });
  }, 60);
}

function closeDrawer(restoreFocus = true) {
  if (!sidebar) return;
  const wasOpen = sidebar.classList.contains('open');
  sidebar.classList.remove('open');
  if (scrim) scrim.classList.remove('show');
  document.body.classList.remove('nav-open');
  if (mainEl) mainEl.inert = false;
  if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');

  if (wasOpen && restoreFocus && lastFocused && typeof lastFocused.focus === 'function') {
    lastFocused.focus({ preventScroll: true });
  }
  lastFocused = null;
}

/* ─── Search helpers ─── */

function clearSearch(focus = true) {
  const input = $('#searchInput');
  if (!input) return;
  input.value = '';
  query = '';
  if (isNotesPage) {
    renderNotes();
    updateNotesUrl();
  }
  if (focus) input.focus();
}

/* ─── Events ─── */

function bindEvents() {
  if (menuBtn) menuBtn.addEventListener('click', openDrawer);
  if (scrim) scrim.addEventListener('click', () => closeDrawer());

  // Any chapter link, anywhere on the dashboard, updates "Continue reading".
  document.addEventListener('click', (event) => {
    const toastTrigger = event.target.closest('[data-toast]');
    if (toastTrigger) showToast(toastTrigger.dataset.toast);

    const noteLink = event.target.closest('a[data-note-file]');
    if (noteLink) saveLastNote(noteLink.dataset.noteFile);
  });

  const filterRow = $('#filterRow');
  if (filterRow) {
    filterRow.addEventListener('click', (event) => {
      const chip = event.target.closest('[data-filter]');
      if (!chip) return;
      setFilter(chip.dataset.filter);
    });
  }

  const searchForm = $('#searchForm');
  const searchInput = $('#searchInput');

  // On the notes page the search filters live; elsewhere the form submits to
  // notes.html?q=… so a search from any page lands on the catalogue.
  if (searchForm) {
    searchForm.addEventListener('submit', (event) => {
      if (!isNotesPage) return;
      event.preventDefault();
      query = searchInput.value.trim().toLowerCase();
      renderNotes();
      updateNotesUrl();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      if (!isNotesPage) return;
      query = searchInput.value.trim().toLowerCase();
      renderNotes();
      updateNotesUrl();
    });
  }

  const clearButton = $('#clearSearch');
  if (clearButton) clearButton.addEventListener('click', () => clearSearch());

  const focusList = $('#focusList');
  if (focusList) {
    focusList.addEventListener('change', (event) => {
      const input = event.target.closest('input[data-focus]');
      if (!input) return;
      const id = input.dataset.focus;
      if (input.checked) focusState[id] = true;
      else delete focusState[id];
      input.closest('.focus-item').classList.toggle('done', input.checked);
      writeJSON(todayKey, focusState);
      updateFocus(true);
    });

    focusList.addEventListener('click', (event) => {
      if (event.target.closest('[data-focus-add]')) {
        openFocusDialog();
        return;
      }
      const edit = event.target.closest('[data-focus-edit]');
      if (edit) openFocusDialog(edit.dataset.focusEdit);
    });
  }

  const focusReset = $('#focusReset');
  if (focusReset) {
    focusReset.addEventListener('click', () => {
      focusState = {};
      writeJSON(todayKey, focusState);
      renderFocus();
      showToast('A fresh page. Small wins to go.');
    });
  }

  const focusChapter = $('#focusChapter');
  if (focusChapter) {
    focusChapter.addEventListener('change', () => {
      const note = noteByFile.get(focusChapter.value);
      if (!note) return;
      const textInput = $('#focusText');
      textInput.value = `Revise ${note.title}`;
      textInput.focus();
      textInput.select();
    });
  }

  const focusForm = $('#focusForm');
  if (focusForm) {
    focusForm.addEventListener('submit', (event) => {
      event.preventDefault();
      submitFocusDialog();
    });
  }

  const focusCancel = $('#focusCancel');
  if (focusCancel) focusCancel.addEventListener('click', closeFocusDialog);

  const focusDelete = $('#focusDelete');
  if (focusDelete) focusDelete.addEventListener('click', deleteFocusTask);

  const focusDialog = $('#focusDialog');
  if (focusDialog) {
    focusDialog.addEventListener('click', (event) => {
      if (event.target === focusDialog) closeFocusDialog();
    });
    focusDialog.addEventListener('close', () => { editingFocusId = null; });
  }

  const lightBtn = $('#lightBtn');
  if (lightBtn) lightBtn.addEventListener('click', () => setTheme('light'));
  const darkBtn = $('#darkBtn');
  if (darkBtn) darkBtn.addEventListener('click', () => setTheme('dark'));
  const footThemeBtn = $('#footThemeBtn');
  if (footThemeBtn) footThemeBtn.addEventListener('click', toggleTheme);

  document.addEventListener('keydown', (event) => {
    const tag = (event.target.tagName || '').toLowerCase();
    const typing = tag === 'input' || tag === 'textarea' || tag === 'select' || event.target.isContentEditable;

    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
      return;
    }

    if (event.key === '/' && !typing) {
      event.preventDefault();
      if (searchInput) searchInput.focus();
      return;
    }

    if (event.key === 'Escape') {
      if (document.body.classList.contains('nav-open')) closeDrawer();
      else if (searchInput && searchInput.value) clearSearch(false);
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900 && document.body.classList.contains('nav-open')) {
      closeDrawer(false);
    }
  });

  const scheme = window.matchMedia('(prefers-color-scheme: dark)');
  const onSchemeChange = (event) => {
    if (!getSavedTheme()) setTheme(event.matches ? 'dark' : 'light', false);
  };
  if (typeof scheme.addEventListener === 'function') scheme.addEventListener('change', onSchemeChange);
  else if (typeof scheme.addListener === 'function') scheme.addListener(onSchemeChange);
}

/* ─── Start ─── */

function init() {
  const navCount = $('#navNotesCount');
  if (navCount) navCount.textContent = String(TOTAL_NOTES);

  const pageCount = $('#pageNoteCount');
  if (pageCount) pageCount.textContent = String(TOTAL_NOTES);

  const libraryCount = $('#libraryCount');
  if (libraryCount) libraryCount.textContent = String(TOTAL_NOTES);

  const footCount = $('#footNoteCount');
  if (footCount) footCount.textContent = String(TOTAL_NOTES);

  const searchInput = $('#searchInput');
  if (searchInput) searchInput.placeholder = `Search ${TOTAL_NOTES} notes — try “demand”`;

  const searchKbd = $('#searchKbd');
  if (searchKbd) searchKbd.textContent = /Mac|iPhone|iPad/.test(navigator.platform) ? '⌘K' : 'Ctrl K';

  if (isNotesPage) {
    readNotesUrl();
    renderFilters();
    renderNotes();
  }

  if ($('#subjectRows')) renderSubjects();

  if ($('#focusList')) {
    populateFocusChapters();
    renderFocus();
  }

  if ($('#continueLink')) {
    renderContinue();
    renderUpNext();
  }

  if ($('#streakDays')) renderStreak();
  if ($('#greetEyebrow')) setDates();
  syncSyllabus();

  setTheme(getSavedTheme() || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'), false);

  bindEvents();

  // Register the shared service worker for offline use.
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./service-worker.js').catch(() => { /* file:// or unsupported */ });
  }
}

init();
