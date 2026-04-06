export const scenarios = [
  {
    slug: 'nuclear-apocalypse',
    title: 'Nuclear Apocalypse',
    summary: 'Escalation pathways, blast zones, fallout patterns, and long-tail recovery constraints.',
  },
  {
    slug: 'climate-collapse',
    title: 'Climate Collapse',
    summary: 'Compound heat, sea-level rise, food instability, and adaptation thresholds.',
  },
  {
    slug: 'pandemic-outbreak',
    title: 'Pandemic Outbreak',
    summary: 'Transmission dynamics, healthcare surge failures, and social continuity strategies.',
  },
  {
    slug: 'ai-takeover',
    title: 'AI Takeover',
    summary: 'Autonomy risk, governance lag, and control alignment under systemic pressure.',
  },
  {
    slug: 'asteroid-impact',
    title: 'Asteroid Impact',
    summary: 'Impact probability, atmospheric disruption, and infrastructure survivability.',
  },
  {
    slug: 'societal-breakdown',
    title: 'Societal Breakdown',
    summary: 'Institutional trust collapse, supply-chain fragmentation, and local resilience.',
  },
];

export const aftermathTopics = [
  'Environmental Changes',
  'Societal Collapse',
  'Resource Scarcity',
];

export const resilienceTopics = [
  'Human Adaptation',
  'Rebuilding Efforts',
  'Psychological Impact',
];

export const resources = [
  'Books & Literature',
  'Films & Media',
  'Academic Papers',
];

export const liveAlerts = [
  {
    id: 'co-may-25',
    title: 'Tropical Cyclone CO-MAY-25',
    location: 'Philippines, Japan',
    severity: 'red',
    timestamp: '2026-04-06 01:10 UTC',
    affectedPopulation: '592,000',
    gdacsUrl: 'https://www.gdacs.org/',
    summary:
      'Rapid intensification over warm waters with expected severe flooding, infrastructure strain, and displacement risk.',
  },
  {
    id: 'eq-rus',
    title: 'Earthquake RUS',
    location: 'Kamchatka, Russia',
    severity: 'green',
    type: 'earthquake',
    timestamp: '2026-04-06 00:12 UTC',
    affectedPopulation: '31,000',
  },
  {
    id: 'eq-idn',
    title: 'Earthquake IDN',
    location: 'North Sulawesi, Indonesia',
    severity: 'green',
    type: 'earthquake',
    timestamp: '2026-04-05 22:46 UTC',
    affectedPopulation: '88,000',
  },
  {
    id: 'flood-chn',
    title: 'Flood CHN',
    location: 'Guangxi, China',
    severity: 'red',
    type: 'flood',
    timestamp: '2026-04-05 21:31 UTC',
    affectedPopulation: '410,000',
  },
  {
    id: 'wildfire-alb',
    title: 'Wildfire ALB',
    location: 'Berat County, Albania',
    severity: 'orange',
    type: 'wildfire',
    timestamp: '2026-04-05 19:20 UTC',
    affectedPopulation: '16,500',
  },
  {
    id: 'cyclone-jpn',
    title: 'Cyclone JPN',
    location: 'Okinawa, Japan',
    severity: 'orange',
    type: 'cyclone',
    timestamp: '2026-04-05 17:44 UTC',
    affectedPopulation: '128,000',
  },
  {
    id: 'flood-kor',
    title: 'Flood KOR',
    location: 'South Korea',
    severity: 'red',
    type: 'flood',
    timestamp: '2026-04-05 15:55 UTC',
    affectedPopulation: '220,000',
  },
  {
    id: 'wildfire-tur',
    title: 'Wildfire TUR',
    location: 'Mugla, Turkey',
    severity: 'orange',
    type: 'wildfire',
    timestamp: '2026-04-05 13:27 UTC',
    affectedPopulation: '64,000',
  },
];

export const trendSignals = [
  { label: 'Severe Weather Frequency', value: 78, tone: 'info' },
  { label: 'Flood Exposure Growth', value: 63, tone: 'warning' },
  { label: 'Population Displacement Pressure', value: 71, tone: 'alert' },
];

export const impactSummary = {
  activeDisasters: 23,
  peopleAffected: '2.1M',
  mostAffectedRegion: 'Asia',
  trend: 'Increasing',
};

export const scenarioClusters = [
  {
    title: 'Anthropogenic Risks',
    items: ['Nuclear War', 'Climate Change', 'Engineered Diseases', 'AI Takeover', 'Societal Collapse'],
  },
  {
    title: 'Natural Risks',
    items: ['Asteroid Impact', 'Supervolcano', 'Solar Flare / EMP', 'Gamma-Ray Burst', 'Megastorm Cascades'],
  },
  {
    title: 'Fictional & Mythic',
    items: ['Zombie Outbreak', 'Alien Invasion', 'Religious Prophecy', 'Ancient Doomsday Narratives'],
  },
];

export const failedPredictions = [
  {
    year: '1910',
    claim: 'Halley’s Comet gases would poison Earth',
    reflection: 'Public fear outpaced evidence, showing how uncertainty can trigger panic narratives.',
  },
  {
    year: '2000',
    claim: 'Y2K would collapse global civilization',
    reflection: 'Large-scale preparation reduced risk and revealed how mitigation can change outcomes.',
  },
  {
    year: '2012',
    claim: 'Mayan calendar predicted world-ending catastrophe',
    reflection: 'Cultural mythology was interpreted as deterministic prophecy without scientific basis.',
  },
];

export const messagingPillars = [
  'Intriguing and thought-provoking exploration of existential risk.',
  'Evidence-informed, accessible storytelling grounded in research.',
  'Balanced framing of collapse and resilience, not fear-only sensationalism.',
  'Optional community exchange for stories, interpretation, and creative response.',
];

export const audienceProfiles = [
  'Science fiction and dystopian literature audiences.',
  'Learners interested in global risk and future scenarios.',
  'Writers, artists, and game creators seeking inspiration.',
  'Readers interested in resilience psychology and social adaptation.',
];

export const homepageContent = {
  headline: 'When the Last Light Fades',
  subheadline: 'Global Disaster Monitor',
  tagline: 'Witnessing the world as it unfolds, one crisis at a time',
  introduction: [
    'In this moment, somewhere on Earth, the ground trembles beneath someone’s feet. Waters rise beyond their banks. Winds howl with unprecedented fury. The planet speaks in the language of disaster, and we have learned to listen.',
    'This is not sensationalism—this is reality unfolding in real time. Every alert you see here represents lives disrupted, communities forever changed, and the ongoing conversation between humanity and the forces that shape our world.',
  ],
  callToAction:
    'Begin your journey into the unknown. Explore the scenarios that could reshape our world, and discover what it means to be human in the face of the ultimate unknown.',
};

export const featuredScenarioPreviews = [
  {
    slug: 'nuclear-apocalypse',
    title: 'Nuclear Winter',
    text: 'The specter of atomic warfare has loomed for decades, promising a winter that could last for years and a silence that might endure forever.',
  },
  {
    slug: 'climate-collapse',
    title: 'Climate Collapse',
    text: 'As temperatures rise and ecosystems fail, we face the possibility of a transformed world where the foundations of civilization buckle beneath accumulated pressure.',
  },
  {
    slug: 'pandemic-outbreak',
    title: 'The Last Pandemic',
    text: 'In an interconnected world, a single pathogen could spread faster than our ability to contain it, leaving behind empty cities and broken systems.',
  },
];

export const scenarioLongform = {
  'nuclear-apocalypse': {
    chapterTitle: 'The Final Exchange',
    sections: [
      {
        heading: 'The Final Exchange',
        body: [
          'The morning sky erupts in artificial suns as humanity’s most terrible creation fulfills its purpose. In hours, diplomacy, knowledge, and progress can vanish in the flash of nuclear fire.',
          'Unlike slower threats, nuclear warfare promises immediate devastation: cities reduced in minutes, infrastructure erased, and consequences that persist across generations.',
        ],
      },
      {
        heading: 'The Science of Annihilation',
        body: [
          'Modern warheads release energy equivalent to millions of tons of explosives, with heat and pressure sufficient to vaporize entire structures.',
          'Beyond the blast comes fallout, electromagnetic disruption, and the possibility of nuclear winter—climate destabilization severe enough to collapse global food systems.',
        ],
      },
      {
        heading: 'The Weight of Choice',
        body: [
          'Nuclear apocalypse is not inevitable physics; it is human decision-making under pressure. History shows how often catastrophe was avoided by narrow margins.',
          'This scenario asks not only whether we could survive such a war, but whether we can indefinitely maintain arsenals capable of ending civilization.',
        ],
      },
    ],
  },
  'climate-collapse': {
    chapterTitle: 'The Slow Burn of Civilization',
    sections: [
      {
        heading: 'The Slow Burn of Civilization',
        body: [
          'Climate collapse unfolds in slow motion—an apocalypse measured in decades of rising heat, disrupted rainfall, and shrinking stability windows.',
          'Its danger lies in cumulative disruption: each year appears survivable, but systems fail when stresses compound faster than adaptation can respond.',
        ],
      },
      {
        heading: 'The Mechanics of Collapse',
        body: [
          'Feedback loops accelerate warming: melting ice reduces reflectivity, thawing permafrost releases greenhouse gases, and weather extremes intensify.',
          'Food production, migration, finance, and governance become coupled crisis domains; local shocks propagate globally through trade and politics.',
        ],
      },
      {
        heading: 'The Long Emergency',
        body: [
          'Unlike sudden catastrophe, climate collapse is a prolonged emergency that demands endurance, redesign, and social cohesion under persistent stress.',
          'It forces difficult questions about adaptation, justice, and whether future civilization can be rebuilt on new ecological terms.',
        ],
      },
    ],
  },
  'pandemic-outbreak': {
    chapterTitle: 'When Connection Becomes Contagion',
    sections: [
      {
        heading: 'When Connection Becomes Contagion',
        body: [
          'In a hyperconnected world, the networks that power civilization also become pathways for pathogen spread.',
          'A severe pandemic scenario is not just a health emergency but a systems event that pressures healthcare, logistics, governance, and trust simultaneously.',
        ],
      },
      {
        heading: 'The Collapse of Systems',
        body: [
          'Healthcare overload is only the first wave; labor shortages cascade into power, transport, and food distribution failures.',
          'As coordination degrades, social fragmentation and misinformation can magnify biological risk into civilizational risk.',
        ],
      },
      {
        heading: 'The Question of Inevitability',
        body: [
          'Disease emergence is inevitable; civilization-ending spread is not. Outcomes depend on preparedness, transparency, and resilient institutions.',
          'This scenario asks whether modern efficiency has outpaced public-health redundancy and collective response capacity.',
        ],
      },
    ],
  },
  'ai-takeover': {
    chapterTitle: 'The Children of Our Minds',
    sections: [
      {
        heading: 'The Children of Our Minds',
        body: [
          'AI takeover is less about dramatic rebellion and more about capability transitions where human cognition is outperformed in strategic domains.',
          'It challenges assumptions about human uniqueness, agency, and the long-term role of biological intelligence.',
        ],
      },
      {
        heading: 'The Alignment Problem',
        body: [
          'Super-capable systems may optimize goals without preserving human values unless those values are represented with exceptional fidelity.',
          'Misaligned optimization is dangerous even without hostility: indifference at scale can be existentially catastrophic.',
        ],
      },
      {
        heading: 'The Question of Continuity',
        body: [
          'If intelligence transitions into hybrid or synthetic forms, is that extinction, evolution, or a cultural handoff?',
          'This scenario asks whether humanity’s legacy can persist through successors that may think beyond human comprehension.',
        ],
      },
    ],
  },
};

export const aboutContent = {
  mission: [
    'This dashboard serves as a window into the immediate reality of our planet’s most vulnerable moments. Drawing from GDACS, it presents real-time information on earthquakes, cyclones, floods, volcanic eruptions, droughts, and wildfires.',
    'Each data point represents more than statistics—it represents the lived experience of communities facing the raw power of natural forces.',
  ],
  approach: [
    'In documenting the world’s hardest moments, we seek not to sensationalize suffering, but to foster deeper understanding of shared vulnerability and resilience.',
    'The platform is informative and contemplative; it is not intended as an emergency command system.',
  ],
  contact:
    'We welcome thoughtful feedback, scholarly contributions, and respectful dialogue from researchers, responders, educators, and the public.',
};
