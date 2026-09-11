# Disclaimer / Vrijwaring

## English

This repository is provided for defensive security awareness and education.

The purpose of the code is to demonstrate why hashing Dutch BSNs
(Burgerservicenummers) with unsalted MD5, SHA-1, or SHA-256 should not be
treated as anonymization. A BSN has a small and enumerable input space, so deterministic
unsalted hashes can be reversed in practice by generating candidate values and
comparing hashes.

Do not use this project to create, publish, share, sell, or distribute BSN
lookup tables, hash reversal tables, or datasets containing generated BSNs and
their hashes. Do not use this project to identify, re-identify, track, or target
individuals.

The scripts only check canonical formatting and the BSN checksum. Even the
all-zero candidate passes that checksum. They do not determine whether a BSN
was actually issued, is currently in use, or belongs to any person.

If you handle BSNs or BSN-derived identifiers, follow applicable privacy,
security, and legal requirements. Prefer avoiding BSN-derived stable identifiers
where possible. When deterministic matching is genuinely required, use an
appropriate design such as a keyed HMAC with a strong secret, strict access
controls, separation of duties, and a documented retention policy.

This is responsible-use guidance, not a licence restriction or legal advice.
The licence governing the software is in [LICENSE](LICENSE). You are
responsible for ensuring that your use is lawful and ethical.

## Nederlands

Deze repository is bedoeld voor defensieve security-awareness en educatie.

Het doel van de code is om te laten zien waarom het hashen van Nederlandse
BSN's (Burgerservicenummers) met unsalted MD5, SHA-1 of SHA-256 niet als
anonimisering moet worden beschouwd. Een BSN heeft een kleine en doorzoekbare
invoerruimte. Daardoor kunnen deterministische hashes zonder salt in de praktijk
worden teruggezocht door kandidaatwaarden te genereren en hashes te vergelijken.

Gebruik dit project niet om BSN-opzoektabellen, hash-reversal-tabellen of
datasets met gegenereerde BSN's en bijbehorende hashes te maken, publiceren,
delen, verkopen of verspreiden. Gebruik dit project niet om personen te
identificeren, opnieuw te identificeren, te volgen of te targeten.

De scripts controleren alleen het canonieke formaat en de BSN-elfproef. Ook
een kandidaat met uitsluitend nullen doorstaat die elfproef. Ze bepalen niet
of een BSN daadwerkelijk is uitgegeven, op dit moment in gebruik is, of aan
een persoon toebehoort.

Als je BSN's of van BSN's afgeleide identifiers verwerkt, volg dan de
toepasselijke privacy-, security- en wettelijke vereisten. Vermijd waar mogelijk
stabiele identifiers die van BSN's zijn afgeleid. Wanneer deterministische
matching echt noodzakelijk is, gebruik dan een passend ontwerp zoals een keyed
HMAC met een sterk geheim, strikte toegangscontrole, functiescheiding en een
gedocumenteerd bewaarbeleid.

Dit is richtlijn voor verantwoord gebruik, geen licentiebeperking of juridisch
advies. De licentie voor de software staat in [LICENSE](LICENSE). Door deze
repository te gebruiken ben je zelf verantwoordelijk om ervoor te zorgen dat
je gebruik rechtmatig en ethisch is.
