---
title: "Spatial-Interactor: Learning Spatial Reasoning through Interaction with the Observable Physical World"
collection: publications
category: manuscripts
permalink: /publication/spatial-interactor
date: 2026-09-18
venue: "arXiv"
authors: >-
  <span class="publication-author">Kaixiang Yao<sup>1,*</sup></span>,
  <span class="publication-author"><strong>Xu Wang<sup>1,*</sup></strong></span>,
  <span class="publication-author">Miao Pan<sup>1</sup></span>,
  <span class="publication-author">Hu Xiyue<sup>1</sup></span>,
  <span class="publication-author">Weishi Wang<sup>2</sup></span>,
  <span class="publication-author">Daniel Dahlmeier<sup>2</sup></span>,
  <span class="publication-author">Jintao Chen<sup>1</sup></span>,
  <span class="publication-author">Yongliang Shen<sup>1</sup></span>,
  <span class="publication-author">Xuhong Zhang<sup>1</sup></span>,
  <span class="publication-author">Wenqi Zhang<sup>1</sup></span>
selected: true

affiliations: >-
  <span><sup>1</sup> Zhejiang University</span>
  <span><sup>2</sup> SAP</span>

video: "https://zju-omniai.github.io/Spatial-Interactor/assets/presentation/spatial-interactor-intro-en.mp4"
video_type: "video/mp4"
poster: "https://zju-omniai.github.io/Spatial-Interactor/assets/presentation/spatial-interactor-intro-poster.webp?v=20260916d"

paperurl: "https://arxiv.org/abs/2609.23038"
projecturl: "https://zju-omniai.github.io/Spatial-Interactor/"
codeurl: "https://github.com/ZJU-OmniAI/Spatial-Interactor"
githubrepo: "ZJU-OmniAI/Spatial-Interactor"
githubstars: 5
dataseturl: "https://huggingface.co/collections/kagakouko/spatial-interactor"
huggingfacedataset: "kagakouko/LSI-108K"
huggingfacedownloads: 348
huggingfacedownloadsdisplay: "348"
paperofdayrank: 2
paperofdayurl: "https://huggingface.co/papers/2609.23038"

abstract: >-
  Spatial reasoning is essential for vision-language models (VLMs) to understand
  and act in the physical world. Reasoning in dynamic environments requires VLMs
  to perceive local state transitions caused by object motion and viewpoint
  changes and integrate them over long trajectories to maintain an updated
  spatial state. However, existing VLMs remain limited in both capabilities.
  Current spatial training primarily focuses on static questions about object
  attributes and spatial relations, providing limited direct supervision for
  state transitions. In contrast, interaction trajectories naturally connect a
  preceding observation, an action, and a subsequent observation, providing
  direct supervision for local state transitions, while complete trajectories
  reveal dependencies among consecutive transitions. We therefore introduce
  **Spatial-Interactor**, a framework that trains VLMs to model physical-world
  state transitions through interaction. We organize this learning process into
  a three-level curriculum covering L1 passive world-state transitions, L2
  active self-state transitions, and L3 long-horizon interaction trajectories.
  Accordingly, we construct the Learning from Spatial Interaction dataset
  (LSI-108K) from simulated and real interaction trajectories, with tasks aligned
  with the objective of each level. Our two-stage training strategy applies
  Supervised Fine-Tuning (SFT) to L1 and L2 for local transition modeling.
  On-Policy Distillation (OPD) then uses privileged self-distillation: a teacher
  branch given segment-level transition descriptions supervises the student's
  on-policy CoT, helping the student learn to integrate consecutive transitions
  over L3 long trajectories. Experiments across multiple VLMs and spatial
  benchmarks show consistent gains in local transition modeling and long-horizon
  integration.

citation: "Kaixiang Yao, Xu Wang, Miao Pan, Hu Xiyue, Weishi Wang, Daniel Dahlmeier, Jintao Chen, Yongliang Shen, Xuhong Zhang, and Wenqi Zhang. (2026). Spatial-Interactor: Learning Spatial Reasoning through Interaction with the Observable Physical World."
---
