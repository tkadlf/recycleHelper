
// 탭 메뉴 토글 기능
document.querySelectorAll('.tab-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();

    const selectedTab = link.dataset.tab;

    // 모든 탭 링크 active 제거 후 클릭한 링크에만 active 추가
    document.querySelectorAll('.tab-link').forEach(el => el.classList.remove('active'));
    link.classList.add('active');

    // 모든 탭 컨텐츠 숨기고 클릭한 탭만 보여주기
    document.querySelectorAll('.tab-content').forEach(sec => {
      sec.classList.toggle('active', sec.id === selectedTab);

    });
  });
});

const fileInput = document.getElementById("fileInput");
  const fileLabel = document.getElementById("fileLabel");

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      const name = fileInput.files[0].name;
      fileLabel.textContent = `선택됨: ${name}`;
      fileLabel.classList.add("file-selected");
    } else {
      fileLabel.textContent = "파일 선택";
      fileLabel.classList.remove("file-selected");
    }
  });

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  const resultsDiv = document.getElementById("results");
  resultsDiv.textContent = "분석 중...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("https://port-0-recyclehelper-mc6bfp4j49e95a8d.sel5.cloudtype.app/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("서버 오류");
    }

    const data = await response.json();
    displayResult(data);
  } catch (err) {
    resultsDiv.textContent = "분석 중 오류가 발생했습니다.";
    console.error(err);
  }
});

function displayResult(data) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  if (data.annotated_image) {
    const img = document.createElement("img");
    img.src = `data:image/png;base64,${data.annotated_image}`;
    img.style.maxWidth = "100%";
    resultsDiv.appendChild(img);
  }

  const classNames = {
    0: "음식물",
    1: "박스",
    2: "유리",
    3: "캔류",
    4: "종이",
    5: "플라스틱",
  };

  if (!data.results || data.results.length === 0) {
    resultsDiv.textContent = "인식된 쓰레기가 없습니다.";
    return;
  }

  const topResult = data.results.sort((a, b) => b.confidence - a.confidence)[0];

  const name = classNames[topResult.class_id] || `클래스 ${topResult.class_id}`;
  const confidence = (topResult.confidence * 100).toFixed(1);
  
  const p = document.createElement("p");
  p.textContent = `🗑️ ${name} (${confidence}%)`;
  resultsDiv.appendChild(p);

}
