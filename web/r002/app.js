"use strict";

const PACKAGE_URL = "../../examples/r002-origin-of-writing.context-package.json";

const REVIEW_META = {
  unreviewed: {
    label: "검토 전",
    tone: "neutral",
    message: "아직 사람의 사료 검토가 시작되지 않았습니다.",
  },
  needs_revision: {
    label: "수정 필요",
    tone: "warning",
    message: "출처는 연결되어 있지만 전문가가 해결해야 할 문제가 남아 있습니다.",
  },
  source_checked: {
    label: "사료 검토 완료",
    tone: "positive",
    message: "인용한 사료와 판본이 사람 검토를 통과했습니다.",
  },
  expert_reviewed: {
    label: "전문가 검토 완료",
    tone: "positive",
    message: "사료뿐 아니라 해석 범위까지 전문가 검토를 통과했습니다.",
  },
};

const CLAIM_META = {
  attested: {
    id: "direct",
    label: "자료가 직접 보여주는 것",
    description: "현재 판본·메타데이터가 명시하는 내용입니다.",
  },
  derived: {
    id: "derived",
    label: "자료 비교로 도출한 결론",
    description: "여러 증거를 연결한 제한적 결론이며 직접 인용과 구분합니다.",
  },
  scholarly_interpretation: {
    id: "scholarship",
    label: "현대 학자의 해석",
    description: "연구자가 제안한 설명이며 다른 견해와 함께 읽어야 합니다.",
  },
  model_inference: {
    id: "model",
    label: "AI 추론",
    description: "탐색을 위한 가설이며 학술 근거로 자동 승격되지 않습니다.",
  },
};

const LAYER_LABELS = {
  artifact: "유물 신원 · 메타데이터",
  transliteration: "전사 · Transliteration",
  translation: "학술 번역",
  edition: "판본",
  image: "이미지",
  secondary: "현대 연구",
};

function createElement(tag, attributes = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attributes)) {
    if (value === null || value === undefined) continue;
    if (key === "className") node.className = value;
    else if (key === "text") node.textContent = String(value);
    else node.setAttribute(key, String(value));
  }
  const normalizedChildren = Array.isArray(children) ? children : [children];
  for (const child of normalizedChildren) {
    if (child === null || child === undefined) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

function evidenceReference(item) {
  return {
    id: item.id,
    recordId: item.source_record_id,
    source: item.source,
    url: item.stable_url,
    locator: item.locator,
    layer: item.layer,
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function buildLearningView(pkg) {
  const evidenceById = new Map(pkg.evidence.map((item) => [item.id, item]));
  const artifacts = new Map();
  const secondarySources = [];

  for (const item of pkg.evidence) {
    const viewItem = {
      ...evidenceReference(item),
      excerpt: item.excerpt,
      attribution: item.attribution,
      licenseManifestId: item.license_manifest_id,
    };
    if (String(item.source_record_id).startsWith("P") && item.layer !== "secondary") {
      if (!artifacts.has(item.source_record_id)) {
        artifacts.set(item.source_record_id, {
          id: item.source_record_id,
          source: item.source,
          url: item.stable_url,
          layers: [],
        });
      }
      artifacts.get(item.source_record_id).layers.push(viewItem);
    } else {
      secondarySources.push(viewItem);
    }
  }

  const lanes = Object.values(CLAIM_META).map((meta) => ({ ...meta, claims: [] }));
  const laneById = new Map(lanes.map((lane) => [lane.id, lane]));
  for (const claim of pkg.claims) {
    const meta = CLAIM_META[claim.status];
    laneById.get(meta.id).claims.push({
      ...claim,
      supportingEvidence: claim.supporting_evidence_ids.map((id) =>
        evidenceReference(evidenceById.get(id)),
      ),
      challengingEvidence: claim.challenging_evidence_ids.map((id) =>
        evidenceReference(evidenceById.get(id)),
      ),
    });
  }

  const nextQuestions = [];
  const debates = pkg.debates.map((debate) => {
    nextQuestions.push(...debate.open_questions);
    return {
      issue: debate.issue,
      positions: debate.positions.map((position) => ({
        summary: position.summary,
        evidence: position.evidence_ids.map((id) =>
          evidenceReference(evidenceById.get(id)),
        ),
      })),
      openQuestions: debate.open_questions,
    };
  });

  const reviewMeta = REVIEW_META[pkg.review.status];
  return {
    id: pkg.id,
    module: { code: "ANE 101 · Module 3", title: "도시와 문자의 탄생" },
    question: pkg.question,
    scope: pkg.question.scope,
    orientation: {
      mapLabel: "우루크와 남부 메소포타미아 — 개념 지도, 축척 아님",
      timeline: [
        {
          label: "Uruk IV",
          range: "ca. 3400–3200 BCE",
          role: "더 이른 기록 단계 — 다음 Source Pack에서 보강",
          active: false,
        },
        {
          label: "Uruk III",
          range: "ca. 3200–3000 BCE",
          role: "현재 세 자료가 속한 비교 범위",
          active: true,
        },
      ],
    },
    artifacts: [...artifacts.values()],
    secondarySources,
    claimLanes: lanes,
    debates,
    uncertainties: pkg.uncertainties.map((item) => ({
      ...item,
      evidence: item.evidence_ids.map((id) => evidenceReference(evidenceById.get(id))),
    })),
    review: {
      ...pkg.review,
      ...reviewMeta,
      humanChecked: ["source_checked", "expert_reviewed"].includes(pkg.review.status),
    },
    provenance: {
      createdAt: pkg.created_at,
      retrievedAt: pkg.retrieval.run_at,
      sourceManifestIds: pkg.retrieval.source_manifest_ids,
      queries: pkg.retrieval.queries,
      softwareVersion: pkg.retrieval.software_version,
    },
    nextQuestions: unique(nextQuestions),
  };
}

function sourceLinks(references) {
  const container = createElement("div", { className: "evidence-links" });
  for (const reference of references) {
    container.append(
      createElement(
        "a",
        {
          className: "evidence-chip",
          href: reference.url,
          target: "_blank",
          rel: "noreferrer",
          title: reference.locator,
          text: `${reference.recordId} · ${reference.layer}`,
        },
      ),
    );
  }
  return container;
}

function renderHeader(view) {
  document.getElementById("module-code").textContent = view.module.code;
  document.getElementById("module-title").textContent = view.module.title;
  document.getElementById("question-title").textContent = view.question.original;
  document.getElementById("normalized-question").textContent = view.question.normalized;

  const statusClasses = `status-chip status-${view.review.tone}`;
  const topStatus = document.getElementById("top-review-status");
  topStatus.className = statusClasses;
  topStatus.textContent = view.review.label;

  const banner = document.getElementById("review-banner");
  banner.className = `review-banner status-${view.review.tone}`;
  document.getElementById("review-label").textContent = view.review.label;
  document.getElementById("review-message").textContent = view.review.message;
  document.getElementById("human-review-badge").textContent = view.review.humanChecked
    ? "사람 검토 연결됨"
    : "전문가 검토 전";

  const chips = document.getElementById("scope-chips");
  const values = [
    ...view.scope.chronology,
    ...view.scope.places,
    ...view.scope.languages,
    ...view.scope.genres,
  ];
  for (const value of values) {
    chips.append(createElement("span", { className: "scope-chip", text: value }));
  }
}

function renderOrientation(view) {
  document.getElementById("map-caption").textContent = view.orientation.mapLabel;
  const timeline = document.getElementById("timeline");
  for (const item of view.orientation.timeline) {
    timeline.append(
      createElement(
        "div",
        { className: `timeline-item${item.active ? " active" : ""}` },
        [
          createElement("strong", { text: `${item.label} · ${item.range}` }),
          createElement("span", { text: item.role }),
        ],
      ),
    );
  }
}

function renderArtifacts(view) {
  const container = document.getElementById("artifact-list");
  for (const artifact of view.artifacts) {
    const layers = createElement("div", { className: "artifact-layers" });
    for (const layer of artifact.layers) {
      const body =
        layer.layer === "transliteration"
          ? createElement("pre", { className: "transliteration", text: layer.excerpt })
          : createElement("p", { text: layer.excerpt });
      layers.append(
        createElement("section", { className: "evidence-layer" }, [
          createElement("p", {
            className: "layer-label",
            text: LAYER_LABELS[layer.layer] || layer.layer,
          }),
          body,
          createElement("div", { className: "source-row" }, [
            createElement("span", { text: layer.locator }),
            createElement(
              "a",
              {
                className: "source-link",
                href: layer.url,
                target: "_blank",
                rel: "noreferrer",
                text: "원자료 확인 ↗",
              },
            ),
          ]),
        ]),
      );
    }

    container.append(
      createElement("article", { className: "artifact-card" }, [
        createElement("header", {}, [
          createElement("div", {}, [
            createElement("p", { className: "panel-kicker", text: "SOURCE-LINKED ARTIFACT" }),
            createElement("h3", { text: artifact.id }),
          ]),
          createElement("span", {
            className: "status-chip status-warning",
            text: "verified 아님",
          }),
        ]),
        layers,
      ]),
    );
  }
}

function renderClaims(view) {
  const container = document.getElementById("claim-lanes");
  for (const lane of view.claimLanes.filter((value) => value.claims.length)) {
    const laneNode = createElement("article", {
      className: "claim-lane",
      "data-lane": lane.id,
    });
    laneNode.append(
      createElement("h3", { text: lane.label }),
      createElement("p", { className: "lane-description", text: lane.description }),
    );

    for (const claim of lane.claims) {
      laneNode.append(
        createElement("section", { className: "claim-card" }, [
          createElement("span", {
            className: "claim-status",
            text: `${claim.confidence} confidence`,
          }),
          createElement("p", { text: claim.statement }),
          createElement("p", { className: "reasoning", text: claim.reasoning }),
          sourceLinks(claim.supportingEvidence),
        ]),
      );
    }
    container.append(laneNode);
  }
}

function renderDebates(view) {
  const container = document.getElementById("debate-list");
  for (const debate of view.debates) {
    const positions = createElement("div", { className: "position-list" });
    for (const position of debate.positions) {
      positions.append(
        createElement("article", { className: "position-card" }, [
          createElement("p", { text: position.summary }),
          sourceLinks(position.evidence),
        ]),
      );
    }

    const questions = createElement("ul", { className: "compact-list" });
    for (const question of debate.openQuestions) {
      questions.append(createElement("li", { text: question }));
    }

    container.append(
      createElement("article", { className: "debate-card" }, [
        createElement("h3", { text: debate.issue }),
        positions,
        createElement("div", { className: "open-question-box" }, [
          createElement("h4", { text: "아직 열린 질문" }),
          questions,
        ]),
      ]),
    );
  }
}

function renderUncertainties(view) {
  const container = document.getElementById("uncertainty-list");
  for (const item of view.uncertainties) {
    container.append(
      createElement("article", { className: "uncertainty-card" }, [
        createElement("h3", { text: `${item.kind} · ${item.target}` }),
        createElement("p", { text: item.description }),
        sourceLinks(item.evidence),
      ]),
    );
  }
}

function appendDefinitionList(list, label, value) {
  list.append(
    createElement("dt", { text: label }),
    createElement("dd", { text: value || "기록 없음" }),
  );
}

function renderProvenance(view) {
  const metadata = document.getElementById("provenance-meta");
  appendDefinitionList(metadata, "패키지 생성", view.provenance.createdAt);
  appendDefinitionList(metadata, "자료 검색", view.provenance.retrievedAt);
  appendDefinitionList(metadata, "소프트웨어", view.provenance.softwareVersion);
  appendDefinitionList(metadata, "Manifest", view.provenance.sourceManifestIds.join(", "));

  const queries = document.getElementById("query-list");
  for (const query of view.provenance.queries) {
    queries.append(createElement("li", { text: query }));
  }

  const reviewDetail = document.getElementById("review-detail");
  reviewDetail.append(
    createElement("p", {
      className: "review-note",
      text: view.review.humanChecked
        ? "사람의 사료 검토가 연결되어 있습니다."
        : "현재는 AI 보조 사료 감사 단계이며 사람 전문가 승인이 없습니다.",
    }),
  );
  const notes = createElement("ul", { className: "compact-list" });
  for (const note of view.review.notes) {
    notes.append(createElement("li", { text: note }));
  }
  reviewDetail.append(notes);
}

function renderNextQuestions(view) {
  const container = document.getElementById("next-question-list");
  for (const question of view.nextQuestions) {
    container.append(createElement("div", { className: "next-question", text: question }));
  }
}

function render(view) {
  renderHeader(view);
  renderOrientation(view);
  renderArtifacts(view);
  renderClaims(view);
  renderDebates(view);
  renderUncertainties(view);
  renderProvenance(view);
  renderNextQuestions(view);
}

async function start() {
  try {
    const response = await fetch(PACKAGE_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Context Package 응답 오류: ${response.status}`);
    const pkg = await response.json();
    render(buildLearningView(pkg));
  } catch (error) {
    const message = document.getElementById("load-error");
    message.hidden = false;
    message.textContent =
      `학습 자료를 불러오지 못했습니다. 저장소 루트에서 ` +
      `python -m http.server 8000을 실행한 뒤 다시 열어 주세요. (${error.message})`;
  }
}

start();
