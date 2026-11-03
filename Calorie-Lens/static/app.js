/* ==========================================================================
   Calorie Lens — Interactive Studio Client Controller
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // State management
  const state = {
    currentImageFile: null,
    currentSamplePath: null,
    currentResult: null,
    activeTab: "mask", // "mask" | "original" | "split"
    activeVessel: "auto", // "auto" | "plate" | "bowl"
    activeMacroMode: "portion", // "portion" | "100g"
    allFoods: [],
  };

  // DOM Elements
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const samplesContainer = document.getElementById("samples-container");
  const vesselPills = document.getElementById("vessel-pills");
  const viewTabs = document.getElementById("view-tabs");
  const loaderOverlay = document.getElementById("loader-overlay");

  const singleView = document.getElementById("single-view");
  const splitView = document.getElementById("split-view");
  const mainDisplayImg = document.getElementById("main-display-img");
  const splitOrigImg = document.getElementById("split-orig-img");
  const splitMaskImg = document.getElementById("split-mask-img");

  const vesselDetectedName = document.getElementById("vessel-detected-name");
  const fillPill = document.getElementById("fill-pill");
  const dishHeadline = document.getElementById("dish-headline");
  const dishCategory = document.getElementById("dish-category");
  const dishFoodType = document.getElementById("dish-food-type");
  const dishConfidence = document.getElementById("dish-confidence");
  const foodOverrideSelect = document.getElementById("food-override-select");
  const predictionsTray = document.getElementById("predictions-tray");

  const caloriesVal = document.getElementById("calories-val");
  const caloriesRangeSub = document.getElementById("calories-range-sub");
  const calDensityTag = document.getElementById("cal-density-tag");
  const calorieUncertaintyBadge = document.getElementById("calorie-uncertainty-badge");

  const portionWeightVal = document.getElementById("portion-weight-val");
  const portionVesselBadge = document.getElementById("portion-vessel-badge");
  const portionAreaVal = document.getElementById("portion-area-val");
  const stdServingVal = document.getElementById("std-serving-val");
  const scaleRatioVal = document.getElementById("scale-ratio-val");

  const tabPortionMacros = document.getElementById("tab-portion-macros");
  const tab100gMacros = document.getElementById("tab-100g-macros");
  const proteinVal = document.getElementById("protein-val");
  const proteinBar = document.getElementById("protein-bar");
  const proteinEnergy = document.getElementById("protein-energy");

  const carbsVal = document.getElementById("carbs-val");
  const carbsBar = document.getElementById("carbs-bar");
  const carbsEnergy = document.getElementById("carbs-energy");

  const fatVal = document.getElementById("fat-val");
  const fatBar = document.getElementById("fat-bar");
  const fatEnergy = document.getElementById("fat-energy");

  const fiberVal = document.getElementById("fiber-val");
  const fiberBar = document.getElementById("fiber-bar");
  const fiberEnergy = document.getElementById("fiber-energy");

  const btnCopySummary = document.getElementById("btn-copy-summary");
  const btnDownloadJson = document.getElementById("btn-download-json");
  const btnDownloadFigure = document.getElementById("btn-download-figure");
  const toastContainer = document.getElementById("toast-container");

  // Show Toast
  function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(10px)";
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  // Fetch all 51 food names
  async function loadFoods() {
    try {
      const res = await fetch("/api/foods");
      const data = await res.json();
      if (data.status === "success") {
        state.allFoods = data.foods;
        foodOverrideSelect.innerHTML = "";
        data.foods.forEach((f) => {
          const opt = document.createElement("option");
          opt.value = f.id;
          opt.textContent = `${f.name} (${f.category})`;
          foodOverrideSelect.appendChild(opt);
        });
      }
    } catch (err) {
      console.error("Failed to load foods:", err);
    }
  }

  // Fetch sample gallery
  async function loadSamples() {
    try {
      const res = await fetch("/api/samples");
      const data = await res.json();
      if (data.status === "success" && data.samples.length > 0) {
        samplesContainer.innerHTML = "";
        data.samples.forEach((sample, idx) => {
          const item = document.createElement("div");
          item.className = "sample-item" + (idx === 0 ? " active" : "");
          item.dataset.path = sample.id;
          item.innerHTML = `
            <img src="${sample.thumbnail}" alt="${sample.title}" loading="lazy">
            <div class="sample-overlay-label">${sample.title}</div>
          `;
          item.addEventListener("click", () => {
            document.querySelectorAll(".sample-item").forEach((el) => el.classList.remove("active"));
            item.classList.add("active");
            state.currentImageFile = null;
            state.currentSamplePath = sample.id;
            triggerAnalysis();
          });
          samplesContainer.appendChild(item);
        });

        // Trigger initial sample analysis
        state.currentSamplePath = data.samples[0].id;
        triggerAnalysis();
      }
    } catch (err) {
      console.error("Failed to load samples:", err);
    }
  }

  // Execute Analysis
  async function triggerAnalysis(foodOverride = null) {
    loaderOverlay.classList.add("active");
    try {
      const formData = new FormData();
      if (state.currentImageFile) {
        formData.append("file", state.currentImageFile);
      } else if (state.currentSamplePath) {
        formData.append("sample_path", state.currentSamplePath);
      } else {
        loaderOverlay.classList.remove("active");
        return;
      }

      if (foodOverride) {
        formData.append("food_id", foodOverride);
      }
      if (state.activeVessel && state.activeVessel !== "auto") {
        formData.append("vessel_type", state.activeVessel);
      }

      const res = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Analysis request failed.");
      }

      const data = await res.json();
      state.currentResult = data.result;
      renderResult(data.result);
      showToast(`Analyzed ${data.result.food_name} portion`);
    } catch (err) {
      console.error(err);
      showToast(`Error: ${err.message}`);
    } finally {
      loaderOverlay.classList.remove("active");
    }
  }

  // Render Result to UI
  function renderResult(result) {
    const n = result.nutrients;
    const p = result.portion;
    const v = result.vessel;

    // 1. Update Images
    mainDisplayImg.src = state.activeTab === "original" ? result.images.original : result.images.mask_overlay;
    splitOrigImg.src = result.images.original;
    splitMaskImg.src = result.images.mask_overlay;

    // 2. Vessel Indicator
    vesselDetectedName.textContent = `${v.name} (${v.diameter_cm}cm)`;
    fillPill.textContent = `Fill: ${p.area_percent}%`;

    // 3. Dish Identification
    dishHeadline.textContent = result.food_name;
    dishCategory.textContent = result.category;
    dishFoodType.textContent = n.food_type.replace("_", " ").toUpperCase();
    dishConfidence.textContent = `${(result.food_conf * 100).toFixed(1)}% Confidence`;

    // Sync select dropdown
    foodOverrideSelect.value = result.food;

    // Top Predictions Tray
    predictionsTray.innerHTML = "";
    if (result.top_predictions && result.top_predictions.length > 0) {
      result.top_predictions.slice(0, 4).forEach((pred) => {
        const pill = document.createElement("div");
        pill.className = "prediction-pill";
        const pct = (pred.confidence * 100).toFixed(1);
        pill.innerHTML = `
          <div class="pred-head">
            <span class="pred-name">${pred.name}</span>
            <span class="pred-conf">${pct}%</span>
          </div>
          <div class="pred-bar-track">
            <div class="pred-bar-fill" style="width: ${pct}%;"></div>
          </div>
        `;
        pill.addEventListener("click", () => {
          triggerAnalysis(pred.food_id);
        });
        predictionsTray.appendChild(pill);
      });
    }

    // 4. Calorie Card
    caloriesVal.textContent = Math.round(n.calories_kcal);
    const [lo, hi] = n.calories_range;
    caloriesRangeSub.innerHTML = `Estimated Range: <strong>${lo} – ${hi} kcal</strong>`;
    calorieUncertaintyBadge.textContent = `±${n.uncertainty_pct}% Uncertainty`;
    calDensityTag.textContent = `Density: ${n.cal_per_g.toFixed(2)} kcal/g (${n.food_type})`;

    // 5. Portion Card
    portionWeightVal.textContent = p.weight_g;
    portionVesselBadge.textContent = `${v.name} Calibrated`;
    portionAreaVal.textContent = `${p.area_percent}%`;
    stdServingVal.textContent = `${p.avg_serving_g} g`;
    scaleRatioVal.textContent = `${p.fill_ratio.toFixed(2)}x`;

    // 6. Macros
    renderMacros(result);
  }

  function renderMacros(result) {
    if (!result) return;
    const n = result.nutrients;
    const isPortion = state.activeMacroMode === "portion";

    if (isPortion) {
      // Current Portion
      proteinVal.textContent = `${n.protein_g.toFixed(1)} g`;
      carbsVal.textContent = `${n.carbohydrates_g.toFixed(1)} g`;
      fatVal.textContent = `${n.fat_g.toFixed(1)} g`;
      fiberVal.textContent = `${n.fiber_g.toFixed(1)} g`;

      const eb = n.energy_breakdown;
      proteinEnergy.textContent = `${(n.protein_g * 4).toFixed(0)} kcal (${eb.protein_pct}%)`;
      carbsEnergy.textContent = `${(n.carbohydrates_g * 4).toFixed(0)} kcal (${eb.carbs_pct}%)`;
      fatEnergy.textContent = `${(n.fat_g * 9).toFixed(0)} kcal (${eb.fat_pct}%)`;
      fiberEnergy.textContent = "Gut health & digestion";

      // Relative bar lengths (normalized to ~60g max)
      proteinBar.style.width = `${Math.min(100, (n.protein_g / 45) * 100)}%`;
      carbsBar.style.width = `${Math.min(100, (n.carbohydrates_g / 70) * 100)}%`;
      fatBar.style.width = `${Math.min(100, (n.fat_g / 35) * 100)}%`;
      fiberBar.style.width = `${Math.min(100, (n.fiber_g / 12) * 100)}%`;
    } else {
      // Standardized per 100g
      const p100 = n.per_100g;
      proteinVal.textContent = `${p100.protein.toFixed(1)} g`;
      carbsVal.textContent = `${p100.carbs.toFixed(1)} g`;
      fatVal.textContent = `${p100.fat.toFixed(1)} g`;
      fiberVal.textContent = `${p100.fiber.toFixed(1)} g`;

      proteinEnergy.textContent = `Ref 100g standard`;
      carbsEnergy.textContent = `Ref 100g standard`;
      fatEnergy.textContent = `Ref 100g standard`;
      fiberEnergy.textContent = `Ref 100g standard`;

      proteinBar.style.width = `${Math.min(100, (p100.protein / 30) * 100)}%`;
      carbsBar.style.width = `${Math.min(100, (p100.carbs / 60) * 100)}%`;
      fatBar.style.width = `${Math.min(100, (p100.fat / 30) * 100)}%`;
      fiberBar.style.width = `${Math.min(100, (p100.fiber / 10) * 100)}%`;
    }
  }

  // Macro toggle listener
  tabPortionMacros.addEventListener("click", () => {
    tabPortionMacros.classList.add("active");
    tab100gMacros.classList.remove("active");
    state.activeMacroMode = "portion";
    renderMacros(state.currentResult);
  });

  tab100gMacros.addEventListener("click", () => {
    tab100gMacros.classList.add("active");
    tabPortionMacros.classList.remove("active");
    state.activeMacroMode = "100g";
    renderMacros(state.currentResult);
  });

  // Food dropdown change listener
  foodOverrideSelect.addEventListener("change", (e) => {
    const selectedId = e.target.value;
    triggerAnalysis(selectedId);
  });

  // Vessel pills listener
  vesselPills.addEventListener("click", (e) => {
    const btn = e.target.closest(".pill-btn");
    if (!btn) return;
    vesselPills.querySelectorAll(".pill-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.activeVessel = btn.dataset.vessel;
    triggerAnalysis(foodOverrideSelect.value);
  });

  // View tabs listener
  viewTabs.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab-btn");
    if (!btn) return;
    viewTabs.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.activeTab = btn.dataset.tab;

    if (state.activeTab === "split") {
      singleView.classList.add("hidden");
      splitView.classList.remove("hidden");
    } else {
      splitView.classList.add("hidden");
      singleView.classList.remove("hidden");
      if (state.currentResult) {
        mainDisplayImg.src =
          state.activeTab === "original"
            ? state.currentResult.images.original
            : state.currentResult.images.mask_overlay;
      }
    }
  });

  // File Upload & Drag and Drop
  dropZone.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      state.currentImageFile = e.target.files[0];
      state.currentSamplePath = null;
      document.querySelectorAll(".sample-item").forEach((el) => el.classList.remove("active"));
      triggerAnalysis();
    }
  });

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      state.currentImageFile = e.dataTransfer.files[0];
      state.currentSamplePath = null;
      document.querySelectorAll(".sample-item").forEach((el) => el.classList.remove("active"));
      triggerAnalysis();
    }
  });

  // Copy Summary Report
  btnCopySummary.addEventListener("click", () => {
    if (!state.currentResult) return;
    const r = state.currentResult;
    const n = r.nutrients;
    const p = r.portion;
    const text = `🍽️ Calorie Lens Report: ${r.food_name} (${r.category})
Serving Weight: ${p.weight_g} g | Vessel: ${r.vessel.name} (Fill: ${p.area_percent}%)
Calories: ${n.calories_kcal} kcal (Range: ${n.calories_range[0]} – ${n.calories_range[1]} kcal, ±${n.uncertainty_pct}%)
Protein: ${n.protein_g} g | Carbs: ${n.carbohydrates_g} g | Fat: ${n.fat_g} g | Fiber: ${n.fiber_g} g
Caloric Density: ${n.cal_per_g} kcal/g (${n.food_type})`;

    navigator.clipboard.writeText(text).then(() => {
      showToast("Report copied to clipboard!");
    });
  });

  // Download JSON
  btnDownloadJson.addEventListener("click", () => {
    if (!state.currentResult) return;
    const stem = state.currentResult.filename.replace(/\.[^/.]+$/, "");
    window.open(`/api/download/json/${encodeURIComponent(stem)}`, "_blank");
  });

  // Download 3-Panel Visual PNG
  btnDownloadFigure.addEventListener("click", () => {
    if (!state.currentResult) return;
    const stem = state.currentResult.filename.replace(/\.[^/.]+$/, "");
    window.open(`/api/download/figure/${encodeURIComponent(stem)}`, "_blank");
  });

  // Initialize
  loadFoods();
  loadSamples();
});
