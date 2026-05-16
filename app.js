const columns = {
  state: "Jurisdiction",
  treatment: "Transit/bus-driver-specific treatment",
  statute: "Statute number(s)",
  covered: "Covered worker/setting",
  trigger: "Statutory language / trigger (condensed from statute)",
  grade: "Felony or misdemeanor",
  punishment: "Punishment / grading",
  distinct: "Distinct from violence in general?",
  sources: "Source URL(s)",
  notes: "Notes"
};

const stateAbbreviations = {
  Alabama: "AL",
  Alaska: "AK",
  Arizona: "AZ",
  Arkansas: "AR",
  California: "CA",
  Colorado: "CO",
  Connecticut: "CT",
  Delaware: "DE",
  "District of Columbia": "DC",
  Florida: "FL",
  Georgia: "GA",
  Hawaii: "HI",
  Idaho: "ID",
  Illinois: "IL",
  Indiana: "IN",
  Iowa: "IA",
  Kansas: "KS",
  Kentucky: "KY",
  Louisiana: "LA",
  Maine: "ME",
  Maryland: "MD",
  Massachusetts: "MA",
  Michigan: "MI",
  Minnesota: "MN",
  Mississippi: "MS",
  Missouri: "MO",
  Montana: "MT",
  Nebraska: "NE",
  Nevada: "NV",
  "New Hampshire": "NH",
  "New Jersey": "NJ",
  "New Mexico": "NM",
  "New York": "NY",
  "North Carolina": "NC",
  "North Dakota": "ND",
  Ohio: "OH",
  Oklahoma: "OK",
  Oregon: "OR",
  Pennsylvania: "PA",
  "Rhode Island": "RI",
  "South Carolina": "SC",
  "South Dakota": "SD",
  Tennessee: "TN",
  Texas: "TX",
  Utah: "UT",
  Vermont: "VT",
  Virginia: "VA",
  Washington: "WA",
  "West Virginia": "WV",
  Wisconsin: "WI",
  Wyoming: "WY"
};

const cacheByState = {
  Arizona: ["az_ch172.html"],
  Colorado: ["co_hb25_1290_page.html", "co_hb25_1290_signed.pdf"],
  Connecticut: ["ct_chap_952.html", "ct_53a_167c.html"],
  Louisiana: ["la_14_34_5_1.html", "la_search.html"],
  Maryland: ["md_7_705.html", "md_7_705_1.html"],
  Michigan: ["mi_750_81e.html", "mi_750_81f.html", "mi_750_81g.html", "mi_search_transit_assault.html", "bing_mi_transit.html"],
  Minnesota: ["mn_609_2231.html", "mn_609_855.html"],
  Tennessee: ["tn_39_13_102.html", "tn_39_13_102_2024.html"],
  Virginia: ["va_18_2_57.html"],
  Washington: ["wa_9a_36_031.html", "wa_9_91_025.html"],
  Wisconsin: ["wi_940_62.html", "wi_940.html", "wi_2025_940_20.html", "wi_940_20.html", "wi_940_20_6m.html", "wi_940_20_full.html", "wi_search.html"],
  "West Virginia": ["wv_61_2_16a.html", "wv_61_2_10b.html"]
};

const els = {
  tableBody: document.querySelector("#table-body"),
  table: document.querySelector("#statute-table"),
  detailPanel: document.querySelector("#detail-panel"),
  stateGrid: document.querySelector("#state-grid"),
  matchCount: document.querySelector("#match-count"),
  search: document.querySelector("#search"),
  lawFilter: document.querySelector("#law-filter"),
  gradingFilter: document.querySelector("#grading-filter"),
  distinctFilter: document.querySelector("#distinct-filter"),
  resetButton: document.querySelector("#reset-button"),
  copyFilteredButton: document.querySelector("#copy-filtered-button"),
  sourceTemplate: document.querySelector("#source-link-template"),
  metrics: {
    total: document.querySelector("#metric-total"),
    transit: document.querySelector("#metric-transit"),
    school: document.querySelector("#metric-school"),
    general: document.querySelector("#metric-general")
  }
};

const state = {
  records: [],
  filtered: [],
  selectedState: null,
  sortKey: columns.state,
  sortDirection: "asc"
};

async function init() {
  try {
    const response = await fetch("bus_driver_violence_statutes.tsv");
    if (!response.ok) {
      throw new Error(`Unable to load TSV: ${response.status}`);
    }
    const text = await response.text();
    state.records = parseTSV(text).map((record) => ({
      ...record,
      category: classifyRecord(record),
      sourceList: splitSources(record[columns.sources])
    }));

    state.selectedState = getInitialState() || state.records[0]?.[columns.state] || null;
    bindEvents();
    applyFilters();
  } catch (error) {
    els.detailPanel.innerHTML = `
      <div class="empty-state">
        <h2>Could not load the data</h2>
        <p>${escapeHTML(error.message)}. Run a local web server from this folder, then open the app through localhost.</p>
      </div>
    `;
  }
}

function parseTSV(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  const headers = lines.shift().split("\t");
  return lines.map((line) => {
    const cells = line.split("\t");
    return headers.reduce((record, header, index) => {
      record[header] = cells[index] || "";
      return record;
    }, {});
  });
}

function bindEvents() {
  [els.search, els.lawFilter, els.gradingFilter, els.distinctFilter].forEach((element) => {
    element.addEventListener("input", applyFilters);
  });

  els.resetButton.addEventListener("click", () => {
    els.search.value = "";
    els.lawFilter.value = "all";
    els.gradingFilter.value = "all";
    els.distinctFilter.value = "all";
    state.sortKey = columns.state;
    state.sortDirection = "asc";
    applyFilters();
    showToast("Filters reset");
  });

  document.querySelectorAll("th button[data-sort]").forEach((button) => {
    button.addEventListener("click", () => {
      const key = button.dataset.sort;
      if (state.sortKey === key) {
        state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
      } else {
        state.sortKey = key;
        state.sortDirection = "asc";
      }
      applyFilters();
    });
  });

  els.copyFilteredButton.addEventListener("click", () => {
    const text = state.filtered
      .map((record) => {
        return `${record[columns.state]}\n${record[columns.statute]}\n${record.sourceList.join("\n")}`;
      })
      .join("\n\n");
    copyText(text, `${state.filtered.length} filtered source set${state.filtered.length === 1 ? "" : "s"} copied`);
  });

  window.addEventListener("hashchange", () => {
    const candidate = decodeURIComponent(window.location.hash.replace(/^#/, ""));
    if (candidate && state.records.some((record) => record[columns.state] === candidate)) {
      selectState(candidate);
    }
  });
}

function applyFilters() {
  const query = els.search.value.trim().toLowerCase();
  const lawFilter = els.lawFilter.value;
  const gradingFilter = els.gradingFilter.value;
  const distinctFilter = els.distinctFilter.value;

  state.filtered = state.records.filter((record) => {
    const haystack = `${Object.values(record).join(" ")} ${record.category}`.toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesLaw = lawFilter === "all" || record.category === lawFilter;
    const matchesGrade = gradingFilter === "all" || gradeMatches(record, gradingFilter);
    const matchesDistinct = distinctFilter === "all" || distinctMatches(record, distinctFilter);
    return matchesQuery && matchesLaw && matchesGrade && matchesDistinct;
  });

  sortRecords();
  if (!state.filtered.some((record) => record[columns.state] === state.selectedState)) {
    state.selectedState = state.filtered[0]?.[columns.state] || state.records[0]?.[columns.state] || null;
  }

  renderMetrics();
  renderStateGrid();
  renderTable();
  renderDetails();
  updateSortIndicators();
}

function sortRecords() {
  const direction = state.sortDirection === "asc" ? 1 : -1;
  state.filtered.sort((a, b) => {
    const aValue = String(readSortValue(a, state.sortKey)).toLowerCase();
    const bValue = String(readSortValue(b, state.sortKey)).toLowerCase();
    return aValue.localeCompare(bValue, undefined, { numeric: true }) * direction;
  });
}

function readSortValue(record, key) {
  if (key === "category") return record.category;
  return record[key] || "";
}

function classifyRecord(record) {
  const treatment = record[columns.treatment].toLowerCase();
  const distinct = record[columns.distinct].toLowerCase();
  const statute = record[columns.statute].toLowerCase();
  const trigger = record[columns.trigger].toLowerCase();

  if (treatment.includes("school-bus only") || distinct.includes("school-bus only")) {
    return "School bus only";
  }
  if (treatment.includes("bus hijacking") || statute.includes("hijacking") || trigger.includes("hijacking")) {
    return "Bus hijacking";
  }
  if (treatment.startsWith("partial") || treatment.includes("local example") || distinct.startsWith("partly")) {
    return "Partial/local";
  }
  if (treatment.includes("interference") || treatment.includes("transit bans") || treatment.includes("exclusion")) {
    return "Transit interference";
  }
  if (treatment.startsWith("no ") || treatment.includes("no public-transit-driver-specific")) {
    return "General only";
  }
  return "Transit-specific";
}

function gradeMatches(record, mode) {
  const grade = `${record[columns.grade]} ${record[columns.punishment]}`.toLowerCase();
  const hasFelony = grade.includes("felony");
  const hasMisdemeanor = grade.includes("misdemeanor");
  if (mode === "felony") return hasFelony;
  if (mode === "misdemeanor") return hasMisdemeanor;
  if (mode === "both") return hasFelony && hasMisdemeanor;
  return true;
}

function distinctMatches(record, mode) {
  const distinct = record[columns.distinct].trim().toLowerCase();
  const no = distinct.startsWith("no");
  if (mode === "yes") return !no;
  if (mode === "no") return no;
  return true;
}

function renderMetrics() {
  const counts = state.records.reduce((acc, record) => {
    acc.total += 1;
    if (record.category === "School bus only") acc.school += 1;
    if (record.category === "General only") acc.general += 1;
    if (!["School bus only", "General only"].includes(record.category)) acc.transit += 1;
    return acc;
  }, { total: 0, transit: 0, school: 0, general: 0 });

  els.metrics.total.textContent = counts.total;
  els.metrics.transit.textContent = counts.transit;
  els.metrics.school.textContent = counts.school;
  els.metrics.general.textContent = counts.general;
  els.matchCount.textContent = `${state.filtered.length} of ${state.records.length} shown`;
}

function renderStateGrid() {
  const filteredNames = new Set(state.filtered.map((record) => record[columns.state]));
  els.stateGrid.innerHTML = state.records
    .map((record) => {
      const name = record[columns.state];
      const abbr = stateAbbreviations[name] || name.slice(0, 2).toUpperCase();
      const active = name === state.selectedState ? "active" : "";
      const hidden = filteredNames.has(name) ? "" : "hidden";
      return `<button class="state-button ${active} ${hidden}" type="button" data-state="${escapeAttribute(name)}" title="${escapeAttribute(name)}">${escapeHTML(abbr)}</button>`;
    })
    .join("");

  els.stateGrid.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => selectState(button.dataset.state));
  });
}

function renderTable() {
  if (!state.filtered.length) {
    els.tableBody.innerHTML = `
      <tr>
        <td colspan="5">
          <strong>No matches.</strong>
          <span class="muted-text"> Try clearing a filter or broadening the search.</span>
        </td>
      </tr>
    `;
    return;
  }

  els.tableBody.innerHTML = state.filtered
    .map((record) => {
      const selected = record[columns.state] === state.selectedState ? "selected" : "";
      return `
        <tr class="${selected}" tabindex="0" data-state="${escapeAttribute(record[columns.state])}">
          <td class="state-cell">${escapeHTML(record[columns.state])}</td>
          <td>${renderTag(record.category)}</td>
          <td class="statute-cell">${escapeHTML(record[columns.statute])}</td>
          <td class="grade-cell">${escapeHTML(record[columns.grade])}</td>
          <td>${escapeHTML(record[columns.distinct])}</td>
        </tr>
      `;
    })
    .join("");

  els.tableBody.querySelectorAll("tr[data-state]").forEach((row) => {
    row.addEventListener("click", () => selectState(row.dataset.state));
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectState(row.dataset.state);
      }
    });
  });
}

function renderDetails() {
  const record = state.records.find((item) => item[columns.state] === state.selectedState);
  if (!record) {
    els.detailPanel.innerHTML = `
      <div class="empty-state">
        <h2>Select a state</h2>
        <p>State-level law summary, caveats, statute trigger, punishment, and source documents will appear here.</p>
      </div>
    `;
    return;
  }

  const cacheFiles = cacheByState[record[columns.state]] || [];
  els.detailPanel.innerHTML = `
    <div class="detail-content">
      <div class="detail-title-row">
        <div>
          <h2>${escapeHTML(record[columns.state])}</h2>
          ${renderTag(record.category)}
        </div>
        <button class="button secondary" type="button" id="copy-state-button">Copy Sources</button>
      </div>

      <section class="detail-section">
        <h3>State Note</h3>
        <p>${escapeHTML(record[columns.treatment])}</p>
        <p class="muted-text">${escapeHTML(record[columns.notes])}</p>
      </section>

      <dl class="detail-list">
        <dt>Statute</dt>
        <dd>${escapeHTML(record[columns.statute])}</dd>
        <dt>Covered</dt>
        <dd>${escapeHTML(record[columns.covered])}</dd>
        <dt>Grade</dt>
        <dd>${escapeHTML(record[columns.grade])}</dd>
        <dt>Punishment</dt>
        <dd>${escapeHTML(record[columns.punishment])}</dd>
        <dt>Distinct</dt>
        <dd>${escapeHTML(record[columns.distinct])}</dd>
      </dl>

      <section class="detail-section">
        <h3>Statutory Trigger</h3>
        <p>${escapeHTML(record[columns.trigger])}</p>
      </section>

      <section class="detail-section">
        <h3>Original Sources</h3>
        <div class="source-list" id="source-list"></div>
      </section>

      <section class="detail-section">
        <h3>Cached Research Files</h3>
        <div class="cache-list" id="cache-list">
          ${
            cacheFiles.length
              ? ""
              : `<p class="muted-text">No local cache file for this state. Use the source links above for the relied-upon source documents.</p>`
          }
        </div>
      </section>
    </div>
  `;

  const sourceList = els.detailPanel.querySelector("#source-list");
  record.sourceList.forEach((url) => sourceList.appendChild(createSourceLink(url, labelForURL(url))));

  const cacheList = els.detailPanel.querySelector("#cache-list");
  cacheFiles.forEach((file) => {
    cacheList.appendChild(createSourceLink(`source_cache/${file}`, file));
  });

  els.detailPanel.querySelector("#copy-state-button").addEventListener("click", () => {
    const text = `${record[columns.state]}\n${record[columns.statute]}\n${record.sourceList.join("\n")}`;
    copyText(text, `${record[columns.state]} sources copied`);
  });
}

function selectState(name) {
  state.selectedState = name;
  if (decodeURIComponent(window.location.hash.replace(/^#/, "")) !== name) {
    history.replaceState(null, "", `#${encodeURIComponent(name)}`);
  }
  renderStateGrid();
  renderTable();
  renderDetails();
}

function renderTag(category) {
  return `<span class="tag ${slugify(category)}">${escapeHTML(category)}</span>`;
}

function createSourceLink(href, label) {
  const node = els.sourceTemplate.content.firstElementChild.cloneNode(true);
  node.href = href;
  node.querySelector(".source-text").textContent = label;
  return node;
}

function splitSources(value) {
  return value
    .split(";")
    .map((source) => source.trim())
    .filter(Boolean);
}

function labelForURL(url) {
  try {
    const parsed = new URL(url);
    const pathParts = parsed.pathname.split("/").filter(Boolean);
    const last = pathParts[pathParts.length - 1] || parsed.hostname;
    if (parsed.hostname.includes("leginfo.legislature.ca.gov")) return `California Legislature: ${parsed.search.replace(/^\?/, "") || "code section"}`;
    if (parsed.hostname.includes("app.leg.wa.gov")) return `Washington RCW: ${parsed.search.replace(/^\?/, "") || last}`;
    if (parsed.hostname.includes("mgaleg.maryland.gov")) return `Maryland Code: ${parsed.search.replace(/^\?/, "")}`;
    if (parsed.hostname.includes("revisor.mn.gov")) return `Minnesota Statutes: ${last}`;
    return `${parsed.hostname}${last ? ` / ${decodeURIComponent(last)}` : ""}`;
  } catch {
    return url;
  }
}

function updateSortIndicators() {
  document.querySelectorAll("th button[data-sort]").forEach((button) => {
    const span = button.querySelector("span");
    const active = button.dataset.sort === state.sortKey;
    span.textContent = active ? (state.sortDirection === "asc" ? "^" : "v") : "";
    button.setAttribute("aria-sort", active ? state.sortDirection : "none");
  });
}

async function copyText(text, message) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(message);
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.className = "visually-hidden";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
    showToast(message);
  }
}

function showToast(message) {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.setAttribute("role", "status");
  toast.textContent = message;
  document.body.appendChild(toast);
  window.setTimeout(() => toast.remove(), 2400);
}

function getInitialState() {
  const hash = decodeURIComponent(window.location.hash.replace(/^#/, ""));
  return hash || null;
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function escapeHTML(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttribute(value) {
  return escapeHTML(value);
}

init();
