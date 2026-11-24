# MeritGate search strategy

## Search intent and page ownership

This is a qualitative query map based on the MeritGate offer and a review of English-language results on 24 November 2026. The phrases are hypotheses to validate against Search Console impressions and meaningful registrations. No search volumes or ranking forecasts have been assigned.

| Landing page | Applicant intent | Query families to measure | Evidence or next action |
| --- | --- | --- | --- |
| / | Discover the programme | study in Portugal with a scholarship, short study abroad in Europe, scholarship programme in Greater Porto, MeritGate EuroPolytech | Programme overview, campus map, route comparison and free interest registration |
| /porto-scholarship/ | Assess the award | merit-based scholarship in Porto, two-month scholarship in Portugal, Porto scholarship selection criteria, what does the Porto scholarship cover | Selection FAQ, costs to confirm and current handbook |
| /study-routes/ | Decide how to participate | British vocational qualification online, study in Porto or online, live online classes with students in Portugal, online route if scholarship unsuccessful | Teaching format, assessment and admissions questions |
| /international-applicants/ | Check readiness | short-term study in Portugal for international students, who can apply to MeritGate, Greater Porto study experience, passport eligibility for study travel | Separate programme selection from travel checks, consult the official travel guidance and contact the academy |

Portugal’s Directorate-General for Higher Education distinguishes short periods of mobility from full cycles of study. University scholarship results also frequently have degree-specific conditions. Erasmus+ vocational mobility has its own institutional application process. These distinctions informed page selection and wording. Broader European study queries can introduce the programme, while the most accurate conversion targets combine location, duration, vocational study and merit-based selection. Do not describe MeritGate as Erasmus+, a university degree or a fully funded scholarship without documented evidence.

Research references:

- https://www.dges.gov.pt/en/pagina/mobility-portugal
- https://www.up.pt/portal/en/live/student-life/scholarships-and-funding/
- https://erasmus-plus.ec.europa.eu/opportunities/individuals/trainees/vocational-education-learners-apprenticeships-and-recent-graduates

## Editorial maintenance

The academy controls the published homepage, programme links and FAQs via Staff Access. The guides carry selected FAQ answers into the build. The introductory copy and page titles live in scripts/seo.py. Review these when the award duration, delivery model or provider changes. Confirm fees, places, deadlines, inclusions and awarding organisations against the approved handbook before describing them as final. Keep the public contact, handbook and venue details visible. Describe a photo once for its visual meaning and keep decorative images silent.

The production site currently serves English. For a translated launch, assign each real translation its own stable language URL, localise all navigation, registration instructions, metadata and scholarship terminology, set its HTML language and self-canonical, then add reciprocal hreflang and sitemap entries for equivalent pages. Prioritise languages using queries, countries and qualified leads. Avoid inventing local campuses or country-specific awards.

## Measurement

Use the verified HTTPS property to compare the most recent complete 28 days against the preceding 28 days once data accumulates. Split brand terms (MeritGate, EuroPolytech and spelling variations) from discovery terms. Group non-brand queries by the four intents above. Examine impressions, clicks, CTR and landing page together. If a page receives impressions for funding coverage but few clicks, first check whether the page really answers the funding question.

Report form submissions from the registration system separately from interest-link clicks. A click indicates intent. A completed form is a lead. Cross-domain attribution to a specific search visit requires a consent-appropriate integration with the external form; do not infer it from Search Console.

The mobile audit workflow measures each public landing page after publication triggered by code changes and can be run manually. Inspect the Lighthouse report and the real-user Core Web Vitals report separately. Evaluate field LCP, INP and CLS at the 75th percentile when traffic is sufficient. Target LCP at or below 2.5 seconds, INP at or below 200 milliseconds and CLS at or below 0.1. A lab performance score is not an INP measurement.

For Google AI features and Bing Copilot, publish short direct answers supported by academy terms, link the relevant guide and use consistent names for the provider and location. Monitor Bing Webmaster Tools AI Performance if the academy connects it. FAQ answers remain useful on the page; Google retired the FAQ rich-result feature in 2026.

- https://developers.google.com/search/docs/appearance/core-web-vitals
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/
