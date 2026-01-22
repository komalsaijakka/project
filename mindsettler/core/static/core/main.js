// Scroll behaviour: header hide/show, progress ring, parallax, reveal
(function () {
  const header = document.getElementById("main-header");
  const circle = document.querySelector(".progress-ring__circle");
  const parallaxLayers = document.querySelectorAll(".parallax-layer");
  const reveals = document.querySelectorAll(".reveal, .fade-up, .fade-in, .timeline-step, .hiw-card");


  let lastScrollY = window.scrollY;

  function setupProgress() {
    if (!circle) return null;
    const radius = 16;
    const circumference = 2 * Math.PI * radius;
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;
    return (progress) => {
      const offset = circumference - progress * circumference;
      circle.style.strokeDashoffset = offset;
    };
  }

  const setProgress = setupProgress();

  const onScroll = () => {
    const currentY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight;
    const winHeight = window.innerHeight;
    const maxScroll = docHeight - winHeight || 1;
    if (setProgress) {
      const p = Math.min(1, Math.max(0, currentY / maxScroll));
      setProgress(p);
    }

    if (currentY > lastScrollY + 5 && currentY > 120) {
      header.classList.add("hidden");
    } else if (currentY < lastScrollY - 5) {
      header.classList.remove("hidden");
    }
    lastScrollY = currentY;

    parallaxLayers.forEach((el) => {
      const section = el.parentElement;
      const rect = section.getBoundingClientRect();
      const relY = rect.top + window.scrollY;
      const distance = currentY - relY;
      const speed = 0.15;
      el.style.transform = `translateY(${distance * speed * -0.1}px)`;
    });
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // reveal on scroll
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in-view"));
  }
})();

// Chatbot: toggle + AJAX to Django endpoint
(function () {
  const panel = document.getElementById("chatbot-panel");
  const toggle = document.getElementById("chat-toggle");
  const closeBtn = document.getElementById("chat-close");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");

  if (!panel || !toggle || !form || !input || !log) return;

  function openChat() {
    panel.classList.add("open");
    input.focus();
  }

  function closeChat() {
    panel.classList.remove("open");
  }

  toggle.addEventListener("click", () => {
    if (panel.classList.contains("open")) {
      closeChat();
    } else {
      openChat();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closeChat);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);
    input.value = "";
    input.focus();

    appendMessage("bot", "…");

    try {
      const formData = new FormData();
      formData.append("message", text);

      const res = await fetch("/chatbot-reply/", {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
      });

      const data = await res.json();
      replaceLastBotMessage(data.reply || "Sorry, I could not respond right now.");
    } catch (err) {
      replaceLastBotMessage("Sorry, something went wrong. Please try again.");
    }
  });

  function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.innerHTML = text; // Allow HTML for links
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  function replaceLastBotMessage(text) {
    const messages = log.querySelectorAll(".msg.bot");
    const last = messages[messages.length - 1];
    if (last) last.innerHTML = text;
    log.scrollTop = log.scrollHeight;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
})();

// Journey page scroll animations
document.addEventListener("DOMContentLoaded", () => {
  const journeyElements = document.querySelectorAll(
    ".journey-title, .journey-intro, .timeline-item, .journey-cta"
  );

  if (!journeyElements.length) return;

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate");
        }
      });
    },
    { threshold: 0.2 }
  );

  journeyElements.forEach(el => observer.observe(el));
});

