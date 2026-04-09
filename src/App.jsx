import { useEffect, useMemo, useState } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import {
  aftermathTopics,
  aboutContent,
  impactSummary,
  liveAlerts,
  messagingPillars,
  homepageContent,
  resilienceTopics,
  resources,
  scenarioClusters,
  scenarioLongform,
  scenarios,
  trendSignals,
  failedPredictions,
  audienceProfiles,
  featuredScenarioPreviews,
} from './data/siteContent';

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
const GDACS_ENDPOINT = `${API_BASE}/api/gdacs`;

function HomePage() {
  const [feedEvents, setFeedEvents] = useState(liveAlerts);
  const [feedSummary, setFeedSummary] = useState(impactSummary);
  const [feedError, setFeedError] = useState('');
  const [loadingFeed, setLoadingFeed] = useState(true);
  const [expandedEventId, setExpandedEventId] = useState('');
  const [feedVersion, setFeedVersion] = useState(0);

  useEffect(() => {
    let mounted = true;

    const loadFeed = async () => {
      try {
        const response = await fetch(GDACS_ENDPOINT);
        if (!response.ok) {
          throw new Error(`Dashboard feed request failed (${response.status}).`);
        }
        const payload = await response.json();
        if (!mounted) return;

        if (Array.isArray(payload.events) && payload.events.length > 0) {
          setFeedEvents(payload.events);
          setFeedVersion((n) => n + 1);
        }
        if (payload.summary) {
          setFeedSummary(payload.summary);
        }
        setFeedError(payload.error || '');
      } catch (error) {
        if (!mounted) return;
        setFeedError(error instanceof Error ? error.message : 'Failed to load live feed.');
      } finally {
        if (mounted) setLoadingFeed(false);
      }
    };

    loadFeed();
    const timer = setInterval(loadFeed, 6 * 60 * 1000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  const [latestAlert, ...recentAlerts] = feedEvents;
  const renderedSummary = useMemo(() => feedSummary ?? impactSummary, [feedSummary]);

  const toneLabel = (severity) => {
    if (severity === 'red') return 'CRITICAL ALERT';
    if (severity === 'orange') return 'HIGH ALERT';
    return 'MONITORING';
  };

  const iconForType = (type) => {
    if (type === 'cyclone') return '🌪️';
    if (type === 'flood') return '🌊';
    if (type === 'wildfire') return '🔥';
    if (type === 'earthquake') return '⚡';
    return '⚠️';
  };

  return (
    <>
      <section className="dashboard-hero" aria-labelledby="hero-title">
        <p className="eyebrow">End of the Human World</p>
        <h1 id="hero-title">{homepageContent.headline}</h1>
        <p className="tagline">{homepageContent.subheadline}</p>
        <p>{homepageContent.tagline}</p>
      </section>

      <section aria-labelledby="latest-alert-title">
        <h2 id="latest-alert-title">Latest Alert</h2>
        {loadingFeed && <p className="status-note">Gathering Global Events... Processing disaster data from around the world.</p>}
        {!!feedError && (
          <p className="status-note error-note">
            Connection Lost. The stream of global events is temporarily unavailable. Reconnecting... ({feedError})
          </p>
        )}
        <article className={`card alert-banner severity-${latestAlert.severity}`}>
          <div>
            <p className="badge">{toneLabel(latestAlert.severity)}</p>
            <h3>{latestAlert.title}</h3>
            <p>{latestAlert.summary}</p>
          </div>
          <ul className="meta-list" aria-label="latest alert metadata">
            <li>
              <span>Location</span>
              <strong>{latestAlert.location}</strong>
            </li>
            <li>
              <span>Reported</span>
              <strong>{latestAlert.timestamp}</strong>
            </li>
            <li>
              <span>Affected Population</span>
              <strong>{latestAlert.affectedPopulation}</strong>
            </li>
          </ul>
          <a href={latestAlert.gdacsUrl} target="_blank" rel="noreferrer" className="button-secondary">
            View Full Report
          </a>
          <p className="small-meta alert-message">
            {latestAlert.severity === 'red'
              ? 'Immediate humanitarian response may be required.'
              : latestAlert.severity === 'orange'
                ? 'Significant impact expected.'
                : 'Situation being monitored.'}
          </p>
        </article>
      </section>

      <section aria-labelledby="recent-events-title">
        <h2 id="recent-events-title">Active Disasters (Last 24 Hours)</h2>
        <div className="disaster-grid">
          {recentAlerts.map((alert) => (
            <article
              key={alert.id}
              className={`card interactive-card severity-${alert.severity} ${feedVersion ? 'fade-in' : ''}`}
            >
              <p className="event-icon">{iconForType(alert.type)}</p>
              <p className="badge">{toneLabel(alert.severity)}</p>
              <h3>{alert.title}</h3>
              <p className="small-meta">{alert.timestamp}</p>
              <p className="small-meta">{alert.location}</p>
              <p className="small-meta">Affected: {alert.affectedPopulation}</p>
              <button
                type="button"
                className="inline-button"
                onClick={() => setExpandedEventId((id) => (id === alert.id ? '' : alert.id))}
              >
                {expandedEventId === alert.id ? 'Hide Details' : 'Expand Details'}
              </button>
              {expandedEventId === alert.id && <p className="small-meta">{alert.summary || 'No summary available.'}</p>}
            </article>
          ))}
        </div>
        {recentAlerts.length === 0 && (
          <article className="card">
            <h3>A Moment of Calm</h3>
            <p>
              In this rare instance, no major disasters are currently being reported. These moments of global quiet
              remind us that peace, however temporary, is possible.
            </p>
          </article>
        )}
      </section>

      <section aria-labelledby="trend-title">
        <h2 id="trend-title">Global Impact Summary</h2>
        <p className="status-note">
          The numbers tell a story of a world in constant motion, where stability is the exception and change is the
          rule.
        </p>
        <div className="card summary-panel">
          <article>
            <h3>Active Disasters</h3>
            <p className="metric-number">{renderedSummary.activeDisasters}</p>
            <p className="small-meta">Current events requiring monitoring or response.</p>
          </article>
          <article>
            <h3>People Affected</h3>
            <p className="metric-number">{renderedSummary.peopleAffected}</p>
            <p className="small-meta">Communities touched by disaster in the last 24 hours.</p>
          </article>
          <article>
            <h3>Most Affected Region</h3>
            <p className="metric-number">{renderedSummary.mostAffectedRegion}</p>
            <p className="small-meta">Where the Earth speaks loudest today.</p>
          </article>
          <article>
            <h3>Trend</h3>
            <p className="metric-number">↗ {renderedSummary.trend}</p>
            <p className="small-meta">The trajectory of our collective vulnerability.</p>
          </article>
        </div>
        <div className="card">
          <h3>Disaster Trend Indicators</h3>
          <div className="trend-stack">
            {trendSignals.map((trend) => (
              <article key={trend.label} className="trend-row">
                <header>
                  <h3>{trend.label}</h3>
                  <strong>{trend.value}%</strong>
                </header>
                <div className="trend-track" role="img" aria-label={`${trend.label}: ${trend.value}%`}>
                  <span className={`trend-fill tone-${trend.tone}`} style={{ width: `${trend.value}%` }} />
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section aria-labelledby="featured-scenarios-title">
        <h2 id="featured-scenarios-title">Featured Scenario Previews</h2>
        <div className="card-grid three-col">
          {featuredScenarioPreviews.map((preview) => (
            <article key={preview.slug} className="card interactive-card">
              <h3>{preview.title}</h3>
              <p>{preview.text}</p>
              <Link to={`/scenarios/${preview.slug}`} className="text-link">
                Explore →
              </Link>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="explore-title">
        <h2 id="explore-title">Explore All Scenarios</h2>
        <div className="card-grid three-col">
          {scenarios.slice(0, 4).map((scenario) => (
            <article key={scenario.slug} className="card interactive-card">
              <h3>{scenario.title}</h3>
              <p>{scenario.summary}</p>
              <Link to={`/scenarios/${scenario.slug}`} className="text-link">
                Read scenario →
              </Link>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="why-title">
        <h2 id="why-title">Why This Project Exists</h2>
        <div className="card-grid two-col">
          <article className="card">
            <h3>Messaging Pillars</h3>
            <ul>
              {messagingPillars.map((pillar) => (
                <li key={pillar}>{pillar}</li>
              ))}
            </ul>
          </article>
          <article className="card">
            <h3>Primary Audience</h3>
            <ul>
              {audienceProfiles.map((profile) => (
                <li key={profile}>{profile}</li>
              ))}
            </ul>
          </article>
        </div>
        <article className="card">
          <h3>Call to Action</h3>
          <p>{homepageContent.callToAction}</p>
        </article>
      </section>

      <section aria-labelledby="intro-title">
        <h2 id="intro-title">Introduction</h2>
        <article className="card">
          {homepageContent.introduction.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </article>
      </section>
    </>
  );
}

function ScenariosPage() {
  return (
    <section>
      <h1>Scenarios</h1>
      <p>Investigate six core pathways to systemic collapse, each with timeline and impact framing.</p>
      <div className="card-grid three-col">
        {scenarioClusters.map((cluster) => (
          <article key={cluster.title} className="card">
            <h2>{cluster.title}</h2>
            <ul>
              {cluster.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
      <div className="card-grid two-col">
        {scenarios.map((scenario) => (
          <article key={scenario.slug} className="card interactive-card">
            <h2>{scenario.title}</h2>
            <p>{scenario.summary}</p>
            <Link className="text-link" to={`/scenarios/${scenario.slug}`}>
              Open details
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}

function ScenarioDetail({ title }) {
  const scenario = scenarios.find((entry) => entry.title === title);
  const longform = scenario ? scenarioLongform[scenario.slug] : null;

  return (
    <section>
      <h1>{title}</h1>
      {longform && (
        <article className="card scenario-lead">
          <h2>{longform.chapterTitle}</h2>
          {longform.sections.map((section) => (
            <section key={section.heading}>
              <h3>{section.heading}</h3>
              {section.body.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </section>
          ))}
        </article>
      )}
      <div className="card-grid one-col">
        <article className="card">
          <h2>Overview</h2>
          <p>High-level framing of trigger conditions and first-order disruption effects.</p>
        </article>
        <article className="card">
          <h2>Scientific Basis</h2>
          <p>Current consensus assumptions, modeling constraints, and uncertainty boundaries.</p>
        </article>
        <article className="card">
          <h2>Potential Impact</h2>
          <p>Expected consequences on infrastructure, health, governance, and food-water-energy systems.</p>
        </article>
        <article className="card">
          <h2>Timeline</h2>
          <p>Progression from initial trigger to medium-term stabilization or compounding collapse.</p>
        </article>
        <article className="card">
          <h2>Related Media</h2>
          <p>Curated documentaries, explainers, and research-led references.</p>
        </article>
      </div>
      <p>
        <Link className="text-link" to="/scenarios">
          ← Back to all scenarios
        </Link>
      </p>
    </section>
  );
}

function AftermathPage() {
  return (
    <section>
      <h1>After the End</h1>
      <div className="card-grid three-col">
        {aftermathTopics.map((topic) => (
          <article key={topic} className="card">
            <h2>{topic}</h2>
            <p>Evidence-based synthesis of long-term systemic effects.</p>
          </article>
        ))}
      </div>
      <article className="card timeline">
        <h2>Interactive Timeline (Wireframe)</h2>
        <ol>
          <li>Phase 1: Shock event and infrastructure stress.</li>
          <li>Phase 2: Cascading failures and migration pressure.</li>
          <li>Phase 3: New social equilibria and adaptation systems.</li>
        </ol>
      </article>
    </section>
  );
}

function SurvivalPage() {
  return (
    <section>
      <h1>Survival &amp; Resilience</h1>
      <div className="card-grid three-col">
        {resilienceTopics.map((topic) => (
          <article key={topic} className="card">
            <h2>{topic}</h2>
            <p>Practical patterns and psychological frameworks for continuity planning.</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function CommunityPage() {
  return (
    <section>
      <h1>Community</h1>
      <div className="card-grid two-col">
        <article className="card interactive-card">
          <h2>Discussion Forum</h2>
          <p>Planned moderated topic threads for scenario debate and preparedness exchange.</p>
        </article>
        <article className="card interactive-card">
          <h2>User Stories</h2>
          <p>Planned first-person adaptation stories to humanize resilience choices.</p>
        </article>
      </div>
    </section>
  );
}

function ResourcesPage() {
  return (
    <section>
      <h1>Resources</h1>
      <div className="card-grid three-col">
        {resources.map((resource) => (
          <article key={resource} className="card">
            <h2>{resource}</h2>
            <p>Curated and categorized source material for deeper study.</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function AboutPage() {
  return (
    <section>
      <h1>About</h1>
      <article className="card">
        <h2>Mission Statement</h2>
        {aboutContent.mission.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </article>
      <article className="card">
        <h2>Our Approach</h2>
        {aboutContent.approach.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </article>
      <article className="card">
        <h2>Contact</h2>
        <p>{aboutContent.contact}</p>
        <p>Email: contact@reckonlight.example (placeholder)</p>
      </article>
      <article className="card">
        <h2>Content Direction</h2>
        <p>
          ReckonLight combines scientific context, fictional exploration, and reflective philosophy while avoiding
          sensational panic narratives.
        </p>
      </article>
    </section>
  );
}

function FailedPredictionsPage() {
  return (
    <section>
      <h1>Failed Doomsday Predictions</h1>
      <p>
        Historical false alarms provide critical context: risk communication can fail when uncertainty is framed as
        inevitability.
      </p>
      <div className="card-grid one-col">
        {failedPredictions.map((item) => (
          <article className="card" key={`${item.year}-${item.claim}`}>
            <h2>
              {item.year}: {item.claim}
            </h2>
            <p>{item.reflection}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function NotFoundPage() {
  return (
    <section>
      <h1>Not Found</h1>
      <p>The page you requested does not exist.</p>
      <Link className="text-link" to="/">
        Return Home
      </Link>
    </section>
  );
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/scenarios" element={<ScenariosPage />} />
        {scenarios.map((scenario) => (
          <Route
            key={scenario.slug}
            path={`/scenarios/${scenario.slug}`}
            element={<ScenarioDetail title={scenario.title} />}
          />
        ))}
        <Route path="/aftermath" element={<AftermathPage />} />
        <Route path="/survival-resilience" element={<SurvivalPage />} />
        <Route path="/community" element={<CommunityPage />} />
        <Route path="/resources" element={<ResourcesPage />} />
        <Route path="/failed-predictions" element={<FailedPredictionsPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  );
}
