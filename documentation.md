# The Headies Awards Voting Automation: A Case Study in Online Voting Security

## Who I Am

I am a self-taught data analyst with a focus on automation and data analytics. While I'm not an expert, I have developed practical skills in creating data-driven solutions through continuous learning and hands-on projects. My interests span from AI exploration and statistical analysis to a deep appreciation for afrobeats music. 

My portfolio (https://prince-uwagboe.netlify.app/) primarily showcases my data analysis and automation skills, but as a personal hobby, I enjoy exploring artificial intelligence and its applications. This project represents the intersection of my technical interests with my passion for the Nigerian music industry and afrobeats scene.

## What I Did

I created a sophisticated automation system that successfully manipulated the voting process for the Headies Awards, a major Nigerian music industry award show. The Headies Awards relied on a simple Google Form for their voting system, which I was able to exploit to submit hundreds of votes for specific artists. My program:

Generated realistic African identities with proper names, phone numbers, and email addresses
Submitted votes that appeared to come from real people across multiple African countries
Successfully bypassed all security measures on the voting platform
Maintained a 100% success rate over 500+ form submissions
Directly influenced the actual results of the awards competition

At some point I thought I got caught because the scripts kept failing and I thought they had found a way to finally keep me out, but it turns out they just recreated the questions because the entry IDs changed. That issue was quickly resolved. I did try not to overdo it because I had other things to do, but at the same time I tried to make an impact and honestly see if I could tip the votes in an artist's favor.

NOTE: I wasn't contracted to do this nor do I have any affiliation with any of the said artists. I just used them as examples for this project.

## Why I Did It

As a self-taught data analyst with a love for afrobeats, I was shocked to discover that the Headies Awards—one of the most influential award shows in afrobeats—was using basic Google Forms for voting. This presented both a technical challenge and an opportunity to highlight critical security issues that could affect artists I follow and appreciate. I created this project to:

1. Demonstrate the real-world security vulnerabilities of simple voting platforms
2. Explore practical applications of the automation skills I've been developing
3. Advocate for fairer systems that protect the integrity of awards that impact afrobeats artists
4. Combine my interest in AI and data analysis with my passion for afrobeats
5. Create a meaningful portfolio project that showcases my self-taught technical abilities

## How I Did It

### Creating Realistic Fake Identities

My software generated believable African identities by:
Creating realistic African names based on common naming patterns from Nigeria, Ghana, Kenya, and South Africa
Generating appropriate phone numbers with correct country codes and formats
Creating email addresses that follow common patterns people use
Ensuring no identity was reused within a 2-hour window

For example, it created identities like "Wanguiito Mwangingi" with a Kenyan phone number and "Segunbayo Adeisha" with a Nigerian email address.

### Mimicking Human Behavior

The program didn't just submit forms rapidly like most bots would. Instead, it:
Took random pauses between actions, just like a real person would
Occasionally took longer breaks (as if the person got distracted)
Moved through the form at a human-like pace
Visited the main website first before submitting the form, like a real visitor would

### Avoiding Detection

To prevent the Headies organization from detecting the automated voting, the software:
Used different internet connections by prompting me to switch my VPN regularly
Made each submission look like it was coming from a different web browser
Randomized technical details that websites use to identify users
Handled errors intelligently, backing off when the system might be suspicious

### Tracking Results

The program kept detailed records of:
Every identity it used (stored in used_identities.json)
Its success rate (which reached 100% in my testing)
Statistics about how many votes it submitted

## The Impact on the Nigerian Music Industry

My project exposed vulnerabilities that have far-reaching implications for the Nigerian music industry, where botting has become a major issue affecting artists' careers, award outcomes, and the integrity of music charts.

### What Is Botting in the Nigerian Music Context?

Botting involves using software to manipulate music-related metrics. There are two main types prevalent in Nigeria:

**Voting Bots**: Programs that automatically submit votes in award contests, like the Headies Awards, to influence results.
**Streaming Farms**: Operations that use bots or multiple devices to generate fake streams on platforms like Spotify, Apple Music, or YouTube, making songs appear more popular than they are.

These practices give some artists an unfair advantage, while others struggle to compete fairly.

### How Botting Affects Nigerian Artists

Botting creates significant challenges for Nigerian artists, from skewing award results to distorting chart rankings:

**Unfair Competition**: Streaming farms boost songs to the top of charts, helping artists secure deals and endorsements. This makes it harder for artists with genuine fans to gain visibility. A Reddit user noted, "For uprising artists... it can be tough seeing someone else who 'doesn't deserve it' take your spot" (https://www.reddit.com/r/interestingasfuck/comments/1c4kv8f/how_musicians_and_labels_use_streaming_farms_to/).
**Award Manipulation**: Voting bots can sway award outcomes, as seen with the Headies Awards' vulnerable Google Form system. This undermines the credibility of awards that are critical for artists' recognition and career growth.
**Financial Losses**: Streaming platforms like Spotify may withhold royalties or remove tracks with fake streams, hurting artists who use these services. Globally, fake streams cost the industry $300 million annually (https://businessday.ng/arts-and-life/article/explainer-streaming-farms-black-market-of-music-business/).
**Erosion of Trust**: Fans and artists lose faith in charts and awards when botting is rampant. Nigerian journalist Joey Akan said, "Apple Music Top 100 has become a marketing tool for Nigerian musicians, not an independent curation of the country's listening habits" (https://businessday.ng/arts-and-life/article/explainer-streaming-farms-black-market-of-music-business/).

### Real Cases of Botting in Nigeria

1. **Chad Focus Streaming Fraud**: Nigerian rapper Chad Focus used streaming farms to inflate his streaming numbers and taught others to do the same. His actions led to a 30-month prison sentence for fraud, showing the legal risks of botting (https://thenativemag.com/explained-nigerian-music-streaming-farm/).

2. **BNXN vs. Ruger Feud**: In 2022, artists BNXN and Ruger clashed on X, with BNXN accusing Ruger of using streaming farms to boost his numbers. BNXN stated, "There are streaming farms in Nigeria now. A room where your label bosses pay money to get your songs up by automation, no real fans" (https://notjustok.com/article/streaming-farms-in-nigerian-music-ecosystem/). This feud highlighted how botting creates tension among artists.

3. **Label-Driven Streaming Farms**: Major Nigerian labels reportedly use streaming farms to keep their artists competitive. Olayinka Ezekiel, a Lagos-based digital distributor, explained, "They want the bragging rights. They want to be able to control deals, they want to be able to control figures" (https://thenativemag.com/explained-nigerian-music-streaming-farm/). This systemic use of botting distorts the industry.

## Technical Results

My program demonstrated the critical security flaws in using Google Forms for high-stakes voting:

1. **No Real Identity Verification**: Anyone can create and submit unlimited fake identities
2. **No Effective Rate Limiting**: My software could submit multiple votes by changing connection methods
3. **Poor Bot Detection**: The system couldn't differentiate between my automated program and real humans
4. **No Geographic Restrictions**: Votes could be submitted from anywhere in the world
5. **No Cross-Field Validation**: The system didn't verify relationships between names, emails, and phone numbers

The technical results were impressive:
100% success rate across 500+ form submissions
Created hundreds of unique, realistic-looking African identities
Maintained perfect reliability despite occasional network timeouts
Complete evasion of any security measures
Demonstrated multiple security vulnerabilities in a production voting system

Even when faced with network errors or connection timeouts, the system's retry mechanisms ensured that not a single vote was lost, maintaining a 100% success rate throughout all batches of submissions.

## Ethical Considerations and Disclaimer

### Ethical Considerations

While I did influence actual results, this project was created with the primary goal of exposing vulnerabilities so they could be addressed. By demonstrating this security flaw, I hope to encourage:

1. The Headies Awards to invest in proper voting infrastructure
2. Other organizations to take online voting security seriously
3. The development of better standards for online voting systems
4. Awareness among the public about how easily online voting can be manipulated

### Disclaimer

This project is presented for educational purposes only. I do not endorse or encourage the use of similar techniques to manipulate voting systems or streaming platforms for personal gain. The tools and methods described here demonstrate security vulnerabilities that should be fixed, not exploited.

The music industry should be a fair playing field where artists succeed based on talent and genuine fan support, not technical manipulation. By exposing these vulnerabilities, I aim to contribute to a more secure and fair ecosystem for all artists.

## Conclusion

As a self-taught data analyst and afrobeats enthusiast, this project represents the intersection of my technical interests and passion for afrobeats. My experiment demonstrates why organizations should never use simple Google Forms for high-stakes voting that affects artists' careers and instead invest in proper systems with:

Identity verification
Geographic restrictions
Sophisticated bot detection
Rate limiting and anomaly detection
Cross-field validation

The Nigerian music industry faces real challenges from botting that threaten its integrity and fairness. By highlighting these vulnerabilities as part of my learning journey, I hope to contribute in a small way to encouraging more secure voting systems for music awards.

Through this project, I've been able to apply my self-taught skills in automation and data analysis to a real-world problem while exploring AI-assisted development techniques—combining my professional interests with my personal passion for afrobeats and the Nigerian music scene.

Visit my portfolio at https://prince-uwagboe.netlify.app/ to see more of my data analysis and automation projects that demonstrate my evolving technical skills as a self-taught data analyst!