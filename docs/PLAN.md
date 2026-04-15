# Agent's Internal Memo: Portfolio Structure & Project Nuances

Tämä on muistio minulle (Antigravity) tulevaa toteutusta varten. Tähän on koottu projektien keskeiset myyntivaltit ja tekniset yksityiskohdat, jotta koodin päivitys on nopeaa ja tarkkaa.

## 1. Projekti: CareAssist AI (Top 1)
*   **Narratiivi:** Insinööriratkaisu Suomen sote-haasteisiin.
*   **Tekniset avainsanat:** Event-driven, AWS SQS, Aurora v2, SSNH-standardit, PII-data anonymization.
*   **Highlight:** "Kotihoitajan vapaamuotoisen kirjauksen muuttaminen rakenteelliseksi sote-dataksi."


## 2. Projekti: EngineeringTeam Crew (Top 2)
*   **Narratiivi:** Ohjelmistokehityksen täysi automatisointi.
*   **Tekniset avainsanat:** CrewAI, Claude 3.7 + GPT-4o, Automated design/code/test, Gradio UI generation.
*   **Highlight:** "Tiimi, joka rakentaa valmiita Python-sovelluksia vaatimusten perusteella alle 10 minuutissa."

## 3. Projekti: ContractSense AI (Top 3)
*   **Narratiivi:** SaaS-tuote, jolla on välitön arvo.
*   **Tekniset avainsanat:** Claude 3.7, PDF-parsing, CoT-visualization, PII-masking, Zero-login demo.
*   **Highlight:** "Lakimiestason sopimusriski-analyysi 30 sekunnissa ilman kirjautumista."

## 4. Projekti: Sidekick AI (Top 4)
*   **Narratiivi:** Autonominen työkaluja käyttävä assistentti.
*   **Tekniset avainsanat:** LangGraph, Worker-Evaluator pattern, Playwright browser tools, Python REPL.
*   **Highlight:** "Itsenäinen agentti, joka osaa selata nettiä ja koodata kokeillakseen ratkaisuja."

## 6. Julkaisualustat (Kustannusoptimoitu & Ammattimainen)

Tavoitteena on minimoida kulut (vapaaherran budjetti) säilyttäen silti "Enterprise"-vaikutelman.

| Projekti | Alusta | Kustannusperuste |
| :--- | :--- | :--- |
| **CareAssist AI** | **AWS Serverless** | Lambda & SQS ovat lähes ilmaisia. Aurora v2 on kallis — käytä **Supabase** tai **Neon** free tieriä tietokannalle kalleuden välttämiseksi. |
| **EngineeringTeam** | **Hugging Face Spaces** | Paras alusta Gradio-pohjaisille AI-tiimeille. Ilmainen hosting ja helppo demo. |
| **ContractSense AI** | **Vercel + Render** | Frontend Vercelissä (ilmainen). Backend Renderissä tai AWS Lambdassa. |
| **Sidekick AI** | **Hugging Face Spaces** | Gradio-assistentti on helpoin ja halvin hostata täällä. |
| **Digital Twin (Prod)** | **AWS (S3/CF/Lambda)** | Staattinen sivu S3:ssa + CloudFront on naurettavan halpa. Lambda pysyy free tierissä. |
| **Portfolio-sivusto** | **Vercel** | Nykyinen setup on optimaalinen — täysin ilmainen. |

## Toteutuksen Huomiot (Design & Code)
*   **Väripaletti:** Pysy tiukasti "Electric Blue" -teemassa. Käytä kirkkaita sinisiä korostuksia, mutta pidä tausta syvänä tummana (#0A0A0B -tyyliin).
*   **Komponentit:** Käytä `motion.div` (Framer Motion) animaatioissa. Varmista, että projektikortit ovat interaktiivisia ja näyttävät premium-luokan varjoja (primary color shadow).
*   **Tekstit:** Käytä teknistä mutta selkeää kieltä. Vältä "hype-buzzwordeja" ilman teknistä katetta. Jokaisen projektin kohdalla pitää näkyä, *miksi* se on vaativa (esim. "AWS Serverless vs. Local script").

---
**Valmiina toimintaan heti kun merkki annetaan.**
