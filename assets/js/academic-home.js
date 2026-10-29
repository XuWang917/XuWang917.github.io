(() => {
  const initializePublicationVideos = () => {
    const videos = document.querySelectorAll(
      ".publication-media video[data-autoplay-on-view]"
    );

    if (!videos.length) return;

    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    const touchOnly = window.matchMedia("(hover: none)").matches;
    const states = new WeakMap();

    const attemptPlayback = (video, state) => {
      if (!state.inView || state.userPaused || document.hidden) return;
      video.play().catch(() => {});
    };

    videos.forEach((video) => {
      const state = {
        inView: false,
        userPaused: false,
        retryTimer: null,
      };
      states.set(video, state);

      video.controls = touchOnly || reducedMotion;
      video.addEventListener("pointerdown", () => {
        state.userPaused = true;
      });
      video.addEventListener("play", () => {
        state.userPaused = false;
      });
      video.addEventListener("pause", () => {
        if (!state.inView || state.userPaused || reducedMotion) return;
        window.clearTimeout(state.retryTimer);
        state.retryTimer = window.setTimeout(
          () => attemptPlayback(video, state),
          200
        );
      });

      if (!touchOnly) {
        video.addEventListener("mouseenter", () => {
          video.controls = true;
        });
        video.addEventListener("mouseleave", () => {
          if (!video.matches(":focus-visible")) video.controls = false;
        });
        video.addEventListener("focus", () => {
          video.controls = true;
        });
        video.addEventListener("blur", () => {
          video.controls = false;
        });
      }
    });

    if (reducedMotion) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const video = entry.target;
          const state = states.get(video);

          if (entry.isIntersecting && entry.intersectionRatio >= 0.55) {
            state.inView = true;
            state.userPaused = false;
            attemptPlayback(video, state);
          } else {
            state.inView = false;
            state.userPaused = false;
            window.clearTimeout(state.retryTimer);
            video.pause();
          }
        });
      },
      { threshold: [0, 0.55, 0.8] }
    );

    videos.forEach((video) => observer.observe(video));

    document.addEventListener("visibilitychange", () => {
      videos.forEach((video) => {
        const state = states.get(video);
        if (document.hidden) {
          video.pause();
        } else {
          attemptPlayback(video, state);
        }
      });
    });
  };

  const initializePublicationCards = () => {
    const cards = document.querySelectorAll("[data-publication-card]");

    cards.forEach((card) => {
      const details = card.querySelector(".publication-details");

      if (!details) return;

      const setExpanded = (expanded) => {
        card.classList.toggle("is-expanded", expanded);
        card.setAttribute("aria-expanded", String(expanded));
        details.setAttribute("aria-hidden", String(!expanded));
      };

      const toggle = () => {
        setExpanded(card.getAttribute("aria-expanded") !== "true");
      };

      card.addEventListener("click", (event) => {
        if (
          event.target.closest(
            "a, video, .publication-details"
          )
        ) {
          return;
        }
        toggle();
      });

      card.addEventListener("keydown", (event) => {
        if (event.target !== card || !["Enter", " "].includes(event.key)) {
          return;
        }
        event.preventDefault();
        toggle();
      });
    });
  };

  const initializeGithubStars = () => {
    const starBadges = document.querySelectorAll("[data-github-stars]");
    const requests = new Map();

    starBadges.forEach((badge) => {
      const repository = badge.dataset.githubStars;
      if (!repository) return;

      if (!requests.has(repository)) {
        const encodedRepository = repository
          .split("/")
          .map((part) => encodeURIComponent(part))
          .join("/");

        requests.set(
          repository,
          fetch(`https://api.github.com/repos/${encodedRepository}`, {
            headers: { Accept: "application/vnd.github+json" },
          })
            .then((response) => {
              if (!response.ok) throw new Error("Unable to load GitHub stars");
              return response.json();
            })
            .then((data) => data.stargazers_count)
        );
      }

      requests
        .get(repository)
        .then((count) => {
          if (!Number.isFinite(count)) return;

          const countElement = badge.querySelector("[data-star-count]");
          const formattedCount = new Intl.NumberFormat("en-US", {
            notation: "compact",
            maximumFractionDigits: 1,
          }).format(count);

          if (countElement) countElement.textContent = formattedCount;
          badge.setAttribute("aria-label", `${count} GitHub stars`);
        })
        .catch(() => {});
    });
  };

  const initializeHuggingFaceDownloads = () => {
    const downloadBadges = document.querySelectorAll(
      "[data-huggingface-downloads]"
    );
    const requests = new Map();

    downloadBadges.forEach((badge) => {
      const dataset = badge.dataset.huggingfaceDownloads;
      if (!dataset) return;

      if (!requests.has(dataset)) {
        const [author, datasetName] = dataset.split("/");
        if (!author || !datasetName) return;

        const query = new URLSearchParams({ author, search: datasetName });
        query.append("expand[]", "downloads");
        query.append("expand[]", "downloadsAllTime");

        requests.set(
          dataset,
          fetch(`https://huggingface.co/api/datasets?${query}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error("Unable to load Hugging Face downloads");
              }
              return response.json();
            })
            .then((data) => {
              if (!Array.isArray(data)) return null;
              return data.find((entry) => entry.id === dataset)?.downloadsAllTime;
            })
        );
      }

      requests
        .get(dataset)
        .then((count) => {
          if (!Number.isFinite(count)) return;

          const countElement = badge.querySelector("[data-download-count]");
          const compactCount = Math.floor(count / 100) / 10;
          const formattedCount =
            count >= 1000
              ? `${compactCount.toFixed(Number.isInteger(compactCount) ? 0 : 1)}k`
              : String(count);

          if (countElement) countElement.textContent = formattedCount;
          badge.setAttribute("aria-label", `${count} downloads`);
        })
        .catch(() => {});
    });
  };

  const initializeAcademicHome = () => {
    initializePublicationVideos();
    initializePublicationCards();
    initializeGithubStars();
    initializeHuggingFaceDownloads();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeAcademicHome);
  } else {
    initializeAcademicHome();
  }
})();
