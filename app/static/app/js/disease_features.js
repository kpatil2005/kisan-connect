// Advanced Disease Detection Features

// 1. PDF DOWNLOAD (Backend)
async function downloadPDF(result, imageData) {
  try {
    const response = await fetch('/download-disease-pdf/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        result: result,
        image: imageData
      })
    });
    
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'plant-disease-report-' + Date.now() + '.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } else {
      alert('Failed to generate PDF');
    }
  } catch (error) {
    console.error('PDF Error:', error);
    alert('Failed to generate PDF: ' + error.message);
  }
}

// 2. HISTORY MANAGEMENT
function saveToHistory(result, imageData) {
  const history = JSON.parse(localStorage.getItem('diseaseHistory') || '[]');
  history.unshift({
    id: Date.now(),
    date: new Date().toISOString(),
    disease: result.disease,
    plant: result.plant,
    confidence: result.confidence,
    image: imageData,
    recommendations: result.recommendations
  });
  localStorage.setItem('diseaseHistory', JSON.stringify(history.slice(0, 10)));
}

function loadHistory() {
  return JSON.parse(localStorage.getItem('diseaseHistory') || '[]');
}

function showHistory() {
  const history = loadHistory();
  let html = '<div class="history-list">';
  history.forEach(item => {
    html += `
      <div class="history-item p-3 mb-2 rounded" style="background:#f8fdf9;cursor:pointer" onclick="viewHistoryItem(${item.id})">
        <div class="d-flex gap-3">
          <img src="${item.image}" style="width:60px;height:60px;object-fit:cover;border-radius:8px">
          <div class="flex-grow-1">
            <strong>${item.disease}</strong>
            <small class="d-block text-muted">${new Date(item.date).toLocaleDateString()}</small>
            <span class="badge bg-success">${item.confidence}%</span>
          </div>
        </div>
      </div>
    `;
  });
  html += '</div>';
  return html;
}

// 3. SHARE FUNCTIONALITY
function shareResults(result) {
  const text = `🌿 Plant Disease Detection\n\nDisease: ${result.disease}\nPlant: ${result.plant}\nConfidence: ${result.confidence}%\n\nDetected by AI-Powered Plant Disease Detector`;
  
  if (navigator.share) {
    navigator.share({
      title: 'Plant Disease Detection',
      text: text,
      url: window.location.href
    });
  } else {
    // Fallback
    const shareUrl = `https://wa.me/?text=${encodeURIComponent(text)}`;
    window.open(shareUrl, '_blank');
  }
}

function shareWhatsApp(result) {
  const text = `🌿 *Plant Disease Detection*\n\n*Disease:* ${result.disease}\n*Plant:* ${result.plant}\n*Confidence:* ${result.confidence}%\n\nDetected by AI System`;
  window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
}

function shareEmail(result) {
  const subject = 'Plant Disease Detection Report';
  const body = `Disease: ${result.disease}\nPlant: ${result.plant}\nConfidence: ${result.confidence}%\n\nTreatment:\n${result.recommendations.join('\n')}`;
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

// 4. VOICE RECOMMENDATIONS
function speakRecommendations(recommendations, language = 'en-US') {
  if ('speechSynthesis' in window) {
    const text = recommendations.join('. ');
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    utterance.rate = 0.9;
    speechSynthesis.speak(utterance);
  }
}

function stopSpeaking() {
  if ('speechSynthesis' in window) {
    speechSynthesis.cancel();
  }
}

// 5. MULTI-LANGUAGE TRANSLATION
const translations = {
  'hi': { // Hindi
    'Treatment Recommendations': 'उपचार की सिफारिशें',
    'Confidence': 'विश्वास',
    'Other Possibilities': 'अन्य संभावनाएं'
  },
  'mr': { // Marathi
    'Treatment Recommendations': 'उपचार शिफारसी',
    'Confidence': 'आत्मविश्वास',
    'Other Possibilities': 'इतर शक्यता'
  }
};

async function translateText(text, targetLang) {
  // Using Google Translate API (you'll need to set this up)
  // For now, return original text
  return text;
}

// 6. SEVERITY INDICATOR
function getSeverity(disease, confidence) {
  if (disease.toLowerCase().includes('healthy')) {
    return { level: 'Low', color: '#4caf50', icon: '✅' };
  } else if (confidence > 80) {
    return { level: 'High', color: '#f44336', icon: '🔴' };
  } else if (confidence > 50) {
    return { level: 'Medium', color: '#ff9800', icon: '🟡' };
  } else {
    return { level: 'Low', color: '#4caf50', icon: '🟢' };
  }
}

function displaySeverity(disease, confidence) {
  const severity = getSeverity(disease, confidence);
  return `
    <div class="severity-indicator p-3 rounded mb-3" style="background:${severity.color}20;border-left:4px solid ${severity.color}">
      <div class="d-flex align-items-center gap-2">
        <span style="font-size:1.5rem">${severity.icon}</span>
        <div>
          <strong style="color:${severity.color}">Severity: ${severity.level}</strong>
          <small class="d-block text-muted">Based on AI confidence and disease type</small>
        </div>
      </div>
    </div>
  `;
}

// 7. BATCH UPLOAD (Multiple Images)
let batchImages = [];

function handleBatchUpload(files) {
  batchImages = Array.from(files);
  return batchImages.length;
}

async function analyzeBatch() {
  const results = [];
  for (const file of batchImages) {
    const formData = new FormData();
    formData.append('image', file);
    const response = await fetch('/predict-disease/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': getCookie('csrftoken') }
    });
    results.push(await response.json());
  }
  return results;
}

// 8. EXPERT CONSULTATION
function contactExpert(result) {
  const message = `I need help with plant disease:\n\nDisease: ${result.disease}\nPlant: ${result.plant}\nConfidence: ${result.confidence}%`;
  const phone = '919876543210'; // Replace with actual expert phone number (country code + number, no + or spaces)
  window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`, '_blank');
}

// 9. IMAGE COMPARISON
function saveForComparison(imageData, result) {
  localStorage.setItem('comparisonImage', JSON.stringify({
    image: imageData,
    result: result,
    date: new Date().toISOString()
  }));
}

function loadComparison() {
  return JSON.parse(localStorage.getItem('comparisonImage') || 'null');
}

// Utility
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
