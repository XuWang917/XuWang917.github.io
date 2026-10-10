---
permalink: /
hide_title: true
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

{% include base_path %}

<div class="academic-home">
  <section class="home-intro" aria-labelledby="about-heading">
    <h1 id="about-heading">About Me</h1>
    <p>{{ site.data.home.intro }}</p>
  </section>

  <section id="research" class="home-section" aria-labelledby="publications-heading">
    <div class="section-heading">
      <h2 id="publications-heading">Research</h2>
    </div>

    {% assign selected_publications = site.publications | where: "selected", true | sort: "date" | reverse %}
    {% if selected_publications.size > 0 %}
      {% for post in selected_publications %}
        {% include publication-row.html post=post %}
      {% endfor %}
    {% else %}
      <article class="publication-row publication-row--empty">
        <div class="publication-media publication-media--placeholder">
          <i class="fa-solid fa-file-video" aria-hidden="true"></i>
        </div>
        <div class="publication-content">
          <h3>Publications are being prepared.</h3>
          <p class="publication-summary">
            Each paper can include a video or image preview, title, authors,
            venue, project links, and a concise summary.
          </p>
        </div>
      </article>
    {% endif %}
  </section>

  <section id="education" class="home-section info-section" aria-labelledby="education-heading">
    <h2 id="education-heading">
      <span class="section-emoji" aria-hidden="true">🎓</span>
      Education
    </h2>
    <div class="info-list">
      {% for item in site.data.home.education %}
      <div class="info-entry info-entry--education">
        <time>{{ item.period }}</time>
        <div class="education-content">
          {% if item.logo %}
            <img class="education-logo" src="{{ item.logo | relative_url }}" alt="" aria-hidden="true">
          {% endif %}
          <div class="education-title">
            <strong>{{ item.institution }}</strong>
            <span>{{ item.degree }}</span>
            {% if item.gpa %}<small>{{ item.gpa }}</small>{% endif %}
          </div>
          <div class="education-program">{{ item.program }}</div>
          {% if item.keywords %}
          <div class="education-keywords">
            {% for keyword in item.keywords %}
              <span>{{ keyword }}</span>
            {% endfor %}
          </div>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    </div>
  </section>

  <section id="honors" class="home-section info-section" aria-labelledby="honors-heading">
    <h2 id="honors-heading">
      <span class="section-emoji" aria-hidden="true">🏆</span>
      Honors &amp; Awards
    </h2>
    <div class="honor-list">
      {% for item in site.data.home.honors %}
      <div class="honor-entry">
        <time>{{ item.period }}</time>
        <strong>
          {% if item.url %}
            <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer">{{ item.title }}</a>
          {% else %}
            {{ item.title }}
          {% endif %}
        </strong>
        {% if item.advisor %}
          <span class="honor-advisor">
            (Advised by
            {% if item.advisor_url %}
              <a href="{{ item.advisor_url }}" target="_blank" rel="noopener noreferrer">{{ item.advisor }}</a>
            {% else %}
              {{ item.advisor }}
            {% endif %})
          </span>
        {% endif %}
        {% if item.detail %}<span>({{ item.detail }})</span>{% endif %}
      </div>
      {% endfor %}
    </div>
  </section>
</div>
