const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const qualitySlider = document.getElementById("qualitySlider");
const qualityValue = document.getElementById("qualityValue");
const qualitySection = document.getElementById("qualitySection");
const previewBtn = document.getElementById("previewBtn");
const previewSection = document.getElementById("previewSection");
const previewImg = document.getElementById("previewImg");
const previewMeta = document.getElementById("previewMeta");
const formatRadios = document.querySelectorAll(
  'input[name="formato_a_cambiar"]',
);

dropzone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = fileInput.files[0].name;
    fileName.classList.add("has-file");
    dropzone.classList.add("has-file");
    previewSection.style.display = "none"; // reseteamos el preview si el usuario cambia el archivo
  }
});

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragging");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragging");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragging");
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    fileName.textContent = files[0].name;
    fileName.classList.add("has-file");
    dropzone.classList.add("has-file");
    previewSection.style.display = "none";
  }
});

// el slider de calidad solo tiene sentido para formatos con compresion con perdida
const formatsConCalidad = ["jpg", "jpeg", "webp"];

function actualizarVisibilidadCalidad() {
  const sel = document.querySelector(
    'input[name="formato_a_cambiar"]:checked',
  ).value;
  qualitySection.style.display = formatsConCalidad.includes(sel)
    ? "block"
    : "none";
}

formatRadios.forEach((r) =>
  r.addEventListener("change", () => {
    actualizarVisibilidadCalidad();
    previewSection.style.display = "none"; // reseteamos el preview si cambia el formato
  }),
);

qualitySlider.addEventListener("input", () => {
  qualityValue.textContent = qualitySlider.value;
});

actualizarVisibilidadCalidad(); // ejecutamos al cargar para setear el estado inicial

// llamamos a /preview que convierte y devuelve la imagen como base64 sin descargarla
previewBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Select an image first.");
    return;
  }

  previewBtn.disabled = true;
  previewBtn.querySelector("span").textContent = "Loading...";

  const formData = new FormData();
  formData.append("archivo_del_usuario", fileInput.files[0]);
  formData.append(
    "formato_a_cambiar",
    document.querySelector('input[name="formato_a_cambiar"]:checked').value,
  );
  formData.append("calidad", qualitySlider.value);

  try {
    const res = await fetch("/preview", { method: "POST", body: formData });
    const data = await res.json();

    if (data.error) {
      alert("Error: " + data.error);
    } else {
      previewImg.src = data.preview;
      previewMeta.textContent = `${data.nombre} · ${data.tamano_kb} KB`;
      previewSection.style.display = "block";
    }
  } catch (err) {
    alert("Could not generate preview.");
  } finally {
    previewBtn.disabled = false;
    previewBtn.querySelector("span").textContent = "Preview";
  }
});
