# Xu Wang's Homepage

Source code for [Xu Wang's homepage](https://xuwang917.github.io/).

The site presents my research interests, publications, education, honors, and
profile links in a compact responsive layout. Publication cards support
video previews, paper and project links, live GitHub star counts, and expandable
abstracts.

## Local Development

```bash
export PATH="$HOME/.gem/ruby/2.6.0/bin:$PATH"
bundle _2.4.22_ exec jekyll serve --host 127.0.0.1 --port 4000
```

Then open `http://localhost:4000/`.

## Content

- `_data/home.yml`: introduction, education, and honors
- `_publications/`: publication metadata and abstracts
- `_pages/`: homepage and supporting pages
- `images/` and `videos/`: profile and publication media
- `_sass/layout/_academic_home.scss`: custom homepage layout

## Deployment

The site is deployed to GitHub Pages from the `main` branch through
`.github/workflows/jekyll-build.yml`.

Built from the [Academic Pages](https://github.com/academicpages/academicpages.github.io)
template and released under the MIT License.
