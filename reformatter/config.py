## config file for link checker

## ENDPOIUNTS
endpoints = [
    'https://theprsb.org/wp-content/uploads/2023/11/Wound-assessment-and-treatment-V1.0_reformatted.json?hsCtaTracking=d2e46ff4-e279-4d73-9d47-8ea2a687a030%7Ceec153e2-133f-42ad-8e75-cde1333a9888',
    'https://theprsb.org/wp-content/uploads/2023/11/Treatment-plan-V1.00_reformatted.json?hsCtaTracking=68056d57-4f27-49b1-ac18-e7934d7b49b7%7Cec2c6978-9355-478a-84c2-17b8039d6460',
    'https://theprsb.org/wp-content/uploads/2023/11/Supported-self-care-V1.00_reformatted.json?hsCtaTracking=d2a1dc34-a98a-479a-abcf-4fab72d67dac%7C116af53d-ccf9-46ce-a194-a04ad302bfd2',
    'https://theprsb.org/wp-content/uploads/2023/01/Social-Prescribing-JSON-1.1.json?hsCtaTracking=141a7bf4-7de5-4374-974a-5d67436207ff%7C5c70e59f-bb7b-47df-9b52-8e1e457f5cb0',
    'https://theprsb.org/wp-content/uploads/2023/01/Referral-to-Social-Prescribing-services-JSON-1.1.json?hsCtaTracking=11e151d7-54ef-4689-9032-24fb5cfb435d%7C85f0cdcc-d8e4-47d2-8e0e-e2b26f23476f',
    'https://theprsb.org/wp-content/uploads/2023/01/Message-back-to-GP-and-Referrer-JSON-1.1.json?hsCtaTracking=63b8982e-5992-46f8-814e-1e77173dd8b7%7Cd6b8256b-0e21-4975-8ca1-ecf3e25133b9',
    'https://theprsb.org/wp-content/uploads/2023/05/111Referral_reformatted.json?hsCtaTracking=f35377bb-7c10-454a-9526-182824bfbf9d%7C87c7a418-6d44-481c-8fc0-df72cf967312',
    'https://theprsb.org/wp-content/uploads/2023/05/111Referral_reformatted.json?hsCtaTracking=3574ec9a-4b02-49db-9b61-2eabf891b4f5%7C1266fed9-63ef-4003-8751-00ad67344256',
    'https://theprsb.org/wp-content/uploads/2023/09/Community-Pharmacy-V3.01.03.json?hsCtaTracking=5eabaf51-b2b4-4771-a452-434fb9014163%7C69b4a150-90c9-417c-9f3b-2dbce498ad75',
    'https://theprsb.org/wp-content/uploads/2023/11/Nursing-Care-Needs-Standard-JSON.json?hsCtaTracking=79c52d30-a431-4bcc-8672-9753c7c6ef72%7C57219916-79ed-4cda-a62e-cf8a3b84b993'
]


## REGEX
expressions = [
    r'href="([^"]*)"',
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
]
