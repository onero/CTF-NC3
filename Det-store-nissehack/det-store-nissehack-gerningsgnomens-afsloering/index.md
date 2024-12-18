+++
title = 'Det store nissehack: Gerningsgnomens Afsløring'
categories = ['Forensics']
date = 2024-12-17T18:40:25+01:00
scrollToTop = true
+++

## Challenge Name:

Det store nissehack: Gerningsgnomens Afsløring

## Category:

Det store nissehack

## Challenge Description:

Efter omfattende efterforskning har du samlet flere spor om gerningsgnomens aktiviteter.

Nu har Julens Politi brug for din hjælp til at færdiggøre politirapporten med præcise detaljer om hændelserne og de stjålne data. Kan du sikre, at rapporten bliver komplet og klar til julens retsopgør?

Link til rapportskabelonen: [https://tryhackme.com/jr/nisseh4ck2o24](https://tryhackme.com/jr/nisseh4ck2o24)

## Approach

The final task consists of a comprehensive quiz to consolidate all the information gathered during the previous four tasks:

![quiz](images/start.png)

Here’s how the information was collected and processed:

| Question                                                  | Task answer was found in | Where answer was found              | Answer                                                  |
|-----------------------------------------------------------|--------------------------|-------------------------------------|---------------------------------------------------------|
| Compromised username                                      | 1                        | Auth.log line of login              | Kanelknaser                                             |
| Santa's pin number                                        | 3                        | Final page with Santa intel         | 2412                                                    |
| Rudolph’s intolerance                                     | 3                        | Final page with Santa intel         | gulerødder                                              |
| Keys for Elf postal service codebook                      | 3                        | Final page with Santa intel         | Nissehue, Sukkerstang, Guirlande, Kræmmerhus, Julekugle |
| Santa's private phone number                              | 4                        | Private bin document                | +299 12 34 56                                           |
| Attacker's IP                                             | 1                        | Auth.log line of login              | 209.38.243.124                                          |
| Attacker's email                                          | 2                        | Found on the certificate            | datagnasker@proton.me                                   |
| Domain, the email was used to create<br>a certificate for | 2                        | Site of the task                    | bitbibliotek.dk                                         |
| Attacker's real name                                      | 3                        | Found on his x.com account          | Børge Madsen                                            |
| Attacker's hometown                                       | 3                        | Found on his Stack Overflow account | Fensmark                                                |
| Company the attacker is working for                       | 2                        | Found on the certificate            | Gnomerne Aps                                            |
| Company hometown                                          | 2                        | Found on the certificate            | Ringsted                                                |


With all the answers filled in, the report was successfully completed:

![formula filled out](images/Formular.png)

Upon submission, we received the confirmation of success:

![success](images/success.png)


## Flag
NC3{hU5k_aT_sKr1v3_r4Pp0Rt}

## Reflections and Learnings

This challenge offered valuable insights into forensic investigation and data correlation across multiple sources. Some key takeaways include:

1. Importance of Log Analysis: Leveraging log files such as auth.log proved crucial in tracing malicious activities and identifying compromised credentials and IPs.

2. Using Metadata Effectively: Information embedded in certificates and social media profiles helped piece together the attacker’s identity and affiliations.

3. Holistic Approach: Cross-referencing diverse data sources, such as Stack Overflow, x.com, and internal files, highlighted the necessity of a well-rounded investigation strategy.

4. Patience in Challenges: Systematically solving individual tasks before tackling the final quiz was instrumental in ensuring a thorough understanding of the case.

This challenge was a testament to the power of methodical investigation and the importance of verifying information across multiple channels. It also emphasized the value of documentation and report writing in forensics, which ensures clarity and completeness in presenting findings.