document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("themeToggle");
  const savedTheme = localStorage.getItem("careercompass-theme");
  if (savedTheme === "dark") document.documentElement.dataset.theme = "dark";
  const syncThemeIcon = () => {
    if (!themeToggle) return;
    const dark = document.documentElement.dataset.theme === "dark";
    themeToggle.innerHTML = `<i class="bi ${dark ? "bi-sun" : "bi-moon-stars"}"></i>`;
    themeToggle.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  };
  syncThemeIcon();
  themeToggle?.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("careercompass-theme", next);
    syncThemeIcon();
  });

  const quizForm = document.getElementById("quizForm");
  const questions = [...document.querySelectorAll("[data-question]")];
  const progressBar = document.getElementById("quizProgress");
  const progressText = document.getElementById("progressText");
  if (quizForm && questions.length) {
    const updateProgress = () => {
      const answered = questions.filter((question) => question.querySelector("input:checked")).length;
      const percent = Math.round((answered / questions.length) * 100);
      progressBar.style.width = `${percent}%`;
      progressBar.setAttribute("aria-valuenow", percent);
      progressText.textContent = `${answered} of ${questions.length} answered`;
    };
    quizForm.addEventListener("change", updateProgress);
    quizForm.addEventListener("submit", (event) => {
      const firstMissing = questions.find((question) => !question.querySelector("input:checked"));
      if (firstMissing) {
        event.preventDefault();
        firstMissing.scrollIntoView({ behavior: "smooth", block: "center" });
        firstMissing.classList.add("question-missing");
        window.setTimeout(() => firstMissing.classList.remove("question-missing"), 1800);
      }
    });
  }

  const modalElement = document.getElementById("infoModal");
  if (modalElement && window.bootstrap) {
    const infoModal = new bootstrap.Modal(modalElement);
    document.addEventListener("click", (event) => {
      const trigger = event.target.closest(".info-trigger");
      if (!trigger) return;
      document.getElementById("infoModalKind").textContent = trigger.dataset.infoKind || "Information";
      document.getElementById("infoModalTitle").textContent = trigger.dataset.infoTitle || "Details";
      document.getElementById("infoModalSummary").textContent = trigger.dataset.infoSummary || "Open the detail page to learn more.";
      document.getElementById("infoModalMeta").textContent = trigger.dataset.infoMeta || "";
      document.getElementById("infoModalLink").href = trigger.dataset.infoUrl || "#";
      infoModal.show();
    });
  }

  const fillDatalist = (input, values) => {
    if (!input) return;
    const list = document.getElementById(input.getAttribute("list"));
    if (!list) return;
    list.replaceChildren(...values.map((value) => {
      const option = document.createElement("option");
      option.value = value;
      return option;
    }));
  };

  // A catalogue choice is only a search preference; institution eligibility is
  // still determined by separately stored verified programme offerings.
  document.querySelectorAll(".course-catalog-data").forEach((dataElement) => {
    let catalogue = [];
    try { catalogue = JSON.parse(dataElement.textContent || "[]"); } catch (_) { return; }
    const form = dataElement.closest("form");
    if (!form) return;
    const category = form.querySelector(".course-category-filter");
    const course = form.querySelector(".course-search");
    const list = course && document.getElementById(course.getAttribute("list"));
    if (!course || !list) return;
    const renderCourses = () => {
      const selectedCategory = category ? category.value : "";
      const rows = catalogue.filter((item) => !selectedCategory || item.category === selectedCategory);
      list.replaceChildren(...rows.map((item) => {
        const option = document.createElement("option");
        option.value = item.name;
        option.label = `${item.level} · ${item.category}${item.aliases.length ? ` · ${item.aliases.join(", ")}` : ""}`;
        return option;
      }));
      course.dataset.availableCount = String(rows.length);
    };
    if (category) category.addEventListener("change", renderCourses);
    renderCourses();
  });

  const fetchJSON = async (url) => {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Location data could not be loaded.");
    return response.json();
  };

  document.querySelectorAll(".location-group").forEach((group) => {
    const country = group.querySelector(".location-country");
    const subdivision = group.querySelector(".location-subdivision");
    const city = group.querySelector(".location-city");
    if (!country || !subdivision || !city) return;
    const loadSubdivisions = async (preserve = false) => {
      const prior = preserve ? subdivision.value : "";
      const data = await fetchJSON(`/api/locations/subdivisions?country=${encodeURIComponent(country.value.trim())}`);
      fillDatalist(subdivision, data.subdivisions || []);
      if (!preserve) { subdivision.value = ""; city.value = ""; fillDatalist(city, []); }
      else subdivision.value = prior;
      const label = group.querySelector("label[for='preferredState']");
      if (label && data.label) label.textContent = data.label;
    };
    const loadCities = async (preserve = false) => {
      const prior = preserve ? city.value : "";
      const url = `/api/locations/cities?country=${encodeURIComponent(country.value.trim())}&subdivision=${encodeURIComponent(subdivision.value.trim())}`;
      const data = await fetchJSON(url);
      fillDatalist(city, data.cities || []);
      if (!preserve) city.value = ""; else city.value = prior;
      city.placeholder = (data.cities || []).length ? "Search or type city" : "Type city manually";
    };
    country.addEventListener("change", () => loadSubdivisions(false).catch(() => fillDatalist(subdivision, [])));
    subdivision.addEventListener("change", () => loadCities(false).catch(() => fillDatalist(city, [])));
    if (country.value) loadSubdivisions(true).then(() => subdivision.value && loadCities(true)).catch(() => {});
  });

  const studyScope = document.getElementById("studyScope");
  const preferredCountry = document.getElementById("preferredCountry") || document.querySelector("[data-location-group='explorer'] .location-country");
  if (studyScope && preferredCountry) {
    studyScope.addEventListener("change", () => {
      if (studyScope.value === "India") {
        preferredCountry.value = "India";
        preferredCountry.dispatchEvent(new Event("change"));
      } else if (studyScope.value === "Abroad" && preferredCountry.value === "India") {
        preferredCountry.value = "";
        preferredCountry.dispatchEvent(new Event("change"));
      }
    });
  }

  const loadMore = document.getElementById("loadMoreColleges");
  const explorerForm = document.getElementById("collegeExplorerForm");
  const results = document.getElementById("collegeResults");
  const makeText = (tag, text, className = "") => {
    const element = document.createElement(tag); element.textContent = text;
    if (className) element.className = className;
    return element;
  };
  const appendCollege = (college) => {
    const card = document.createElement("article"); card.className = "match-card college-result-card";
    Object.assign(card.dataset, { collegeSlug: college.slug, collegeName: college.name,
      collegeLocation: `${college.city}, ${college.state}, ${college.country}`,
      collegeCourse: college.matched_course, collegeType: college.ownership, collegeFee: college.fees });
    const body = document.createElement("div"); body.className = "flex-grow-1";
    const badges = document.createElement("div"); badges.className = "d-flex flex-wrap gap-2 align-items-center";
    badges.append(makeText("span", college.country === "India" ? "India" : "Abroad", "region-badge"), makeText("span", college.ownership, "status-badge"), makeText("span", college.budget_status, "status-badge"));
    body.append(badges, makeText("h3", college.name, "h5 mt-2 mb-1"), makeText("p", `${college.city}, ${college.state}, ${college.country}`, "text-secondary mb-2"), makeText("p", `Course match: ${college.matched_course}`, "mb-2"), makeText("p", `Tuition: ${college.fees}`, "small mb-2"));
    if (college.ranking_info) body.append(makeText("p", `Verified indicator: ${college.ranking_info}`, "small mb-2"));
    const actions = document.createElement("div"); actions.className = "college-card-actions";
    const shortlist = makeText("button", " Shortlist", "btn btn-outline-dark btn-sm shortlist-toggle");
    shortlist.type = "button"; shortlist.prepend(Object.assign(document.createElement("i"), { className: "bi bi-bookmark-plus" })); actions.append(shortlist);
    [[`/colleges/${college.slug}`, "Details", "btn btn-primary btn-sm"], [college.official_url, "Official site", "btn btn-outline-primary btn-sm"], [college.admission_url, "Admissions", "btn btn-outline-secondary btn-sm"]].forEach(([href, label, classes], index) => { const link = makeText("a", label, classes); link.href = href; if (index) { link.target = "_blank"; link.rel = "noopener"; } actions.append(link); });
    card.append(body, actions); results.append(card);
  };
  if (loadMore && explorerForm && results) {
    loadMore.addEventListener("click", async () => {
      loadMore.disabled = true; loadMore.textContent = "Loading…";
      const params = new URLSearchParams(new FormData(explorerForm));
      params.set("page", results.dataset.nextPage || "2");
      try {
        const data = await fetchJSON(`/api/colleges/search?${params.toString()}`);
        data.results.forEach(appendCollege);
        results.dataset.nextPage = String(data.page + 1);
        if (!data.has_more) loadMore.remove();
        else { loadMore.disabled = false; loadMore.textContent = "Load more verified results"; }
      } catch (error) {
        loadMore.disabled = false; loadMore.textContent = "Try loading more again";
      }
    });
  }

  const shortlistKey = "careercompass-shortlist-v1";
  const shortlistBar = document.getElementById("shortlistBar");
  const shortlistCount = document.getElementById("shortlistCount");
  const shortlistItems = document.getElementById("shortlistItems");
  const getShortlist = () => {
    try { return JSON.parse(localStorage.getItem(shortlistKey) || "[]"); } catch (_) { return []; }
  };
  const saveShortlist = (items) => localStorage.setItem(shortlistKey, JSON.stringify(items.slice(0, 6)));
  const renderShortlist = () => {
    const items = getShortlist();
    if (shortlistBar) shortlistBar.hidden = items.length === 0;
    if (shortlistCount) shortlistCount.textContent = String(items.length);
    document.querySelectorAll(".shortlist-toggle").forEach((button) => {
      const card = button.closest("[data-college-slug]");
      const saved = card && items.some((item) => item.slug === card.dataset.collegeSlug);
      button.classList.toggle("active", Boolean(saved));
      button.innerHTML = saved ? '<i class="bi bi-bookmark-check-fill"></i> Saved' : '<i class="bi bi-bookmark-plus"></i> Shortlist';
    });
    if (!shortlistItems) return;
    shortlistItems.replaceChildren(...(items.length ? items.map((item) => {
      const row = document.createElement("article"); row.className = "shortlist-item";
      const copy = document.createElement("div");
      copy.append(makeText("h3", item.name, "h6 mb-1"), makeText("p", item.location, "small text-secondary mb-2"), makeText("span", item.course, "tag-chip"), makeText("span", item.type, "tag-chip ms-1"), makeText("p", item.fee, "small mt-2 mb-0"));
      const actions = document.createElement("div"); actions.className = "d-grid gap-2";
      const details = makeText("a", "View details", "btn btn-primary btn-sm"); details.href = `/colleges/${item.slug}`;
      const remove = makeText("button", "Remove", "btn btn-outline-danger btn-sm"); remove.type = "button";
      remove.addEventListener("click", () => { saveShortlist(getShortlist().filter((saved) => saved.slug !== item.slug)); renderShortlist(); });
      actions.append(details, remove); row.append(copy, actions); return row;
    }) : [makeText("p", "No colleges saved yet. Use the Shortlist button on any college card.", "text-secondary text-center py-4")]));
  };
  document.addEventListener("click", (event) => {
    const button = event.target.closest(".shortlist-toggle");
    if (!button) return;
    const card = button.closest("[data-college-slug]"); if (!card) return;
    let items = getShortlist(); const slug = card.dataset.collegeSlug;
    if (items.some((item) => item.slug === slug)) items = items.filter((item) => item.slug !== slug);
    else items.push({ slug, name: card.dataset.collegeName, location: card.dataset.collegeLocation,
      course: card.dataset.collegeCourse, type: card.dataset.collegeType, fee: card.dataset.collegeFee });
    saveShortlist(items); renderShortlist();
  });
  document.getElementById("clearShortlist")?.addEventListener("click", () => { saveShortlist([]); renderShortlist(); });
  renderShortlist();
});
