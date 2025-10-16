-- =====================================================
-- 1️⃣ BANKING SOURCES
-- =====================================================
DROP TABLE IF EXISTS public.banking_sources CASCADE;
CREATE TABLE public.banking_sources (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

INSERT INTO public.banking_sources (id, name, description)
VALUES
('RBK', 'Retail Banking', 'Where customer accounts are stored'),
('GTD', 'Transaction Banking', 'Corporate and institutional payments'),
('REM', 'Remittance', 'Money transfer for domestic and international remittances'),
('LNS', 'Loan Systems', 'Where customer loan info and disbursement details are stored'),
('VSB', 'Visa Systems', 'Where credit card transactions are stored'),
('BWC', 'BankWide CIF', 'Where customer information is stored'),
('SKN', 'Settlement System', 'Handles interbank clearing and settlements'),
('FIS', 'Information Services', 'Financial data services');

-- =====================================================
-- 2️⃣ COUNTRIES
-- =====================================================
DROP TABLE IF EXISTS public.countries CASCADE;
CREATE TABLE public.countries (
  code CHAR(2) PRIMARY KEY,
  name TEXT NOT NULL,
  risk_tier TEXT DEFAULT 'Low',
  is_sanctioned BOOLEAN DEFAULT FALSE
);

INSERT INTO public.countries (code, name)
VALUES
('AF', 'Afghanistan'),
('AL', 'Albania'),
('DZ', 'Algeria'),
('AS', 'American Samoa'),
('AD', 'Andorra'),
('AO', 'Angola'),
('AI', 'Anguilla'),
('AQ', 'Antarctica'),
('AG', 'Antigua and Barbuda'),
('AR', 'Argentina'),
('AM', 'Armenia'),
('AW', 'Aruba'),
('AU', 'Australia'),
('AT', 'Austria'),
('AZ', 'Azerbaijan'),
('BS', 'Bahamas (the)'),
('BH', 'Bahrain'),
('BD', 'Bangladesh'),
('BB', 'Barbados'),
('BY', 'Belarus'),
('BE', 'Belgium'),
('BZ', 'Belize'),
('BJ', 'Benin'),
('BM', 'Bermuda'),
('BT', 'Bhutan'),
('BO', 'Bolivia (Plurinational State of)'),
('BQ', 'Bonaire, Sint Eustatius and Saba'),
('BA', 'Bosnia and Herzegovina'),
('BW', 'Botswana'),
('BV', 'Bouvet Island'),
('BR', 'Brazil'),
('IO', 'British Indian Ocean Territory (the)'),
('BN', 'Brunei Darussalam'),
('BG', 'Bulgaria'),
('BF', 'Burkina Faso'),
('BI', 'Burundi'),
('CV', 'Cabo Verde'),
('KH', 'Cambodia'),
('CM', 'Cameroon'),
('CA', 'Canada'),
('KY', 'Cayman Islands (the)'),
('CF', 'Central African Republic (the)'),
('TD', 'Chad'),
('CL', 'Chile'),
('CN', 'China'),
('CX', 'Christmas Island'),
('CC', 'Cocos (Keeling) Islands (the)'),
('CO', 'Colombia'),
('KM', 'Comoros (the)'),
('CD', 'Congo (the Democratic Republic of the)'),
('CG', 'Congo (the)'),
('CK', 'Cook Islands (the)'),
('CR', 'Costa Rica'),
('HR', 'Croatia'),
('CU', 'Cuba'),
('CW', 'Curaçao'),
('CY', 'Cyprus'),
('CZ', 'Czechia'),
('CI', 'Côte d''Ivoire'),
('DK', 'Denmark'),
('DJ', 'Djibouti'),
('DM', 'Dominica'),
('DO', 'Dominican Republic (the)'),
('EC', 'Ecuador'),
('EG', 'Egypt'),
('SV', 'El Salvador'),
('GQ', 'Equatorial Guinea'),
('ER', 'Eritrea'),
('EE', 'Estonia'),
('SZ', 'Eswatini'),
('ET', 'Ethiopia'),
('FK', 'Falkland Islands (the) [Malvinas]'),
('FO', 'Faroe Islands (the)'),
('FJ', 'Fiji'),
('FI', 'Finland'),
('FR', 'France'),
('GF', 'French Guiana'),
('PF', 'French Polynesia'),
('TF', 'French Southern Territories (the)'),
('GA', 'Gabon'),
('GM', 'Gambia (the)'),
('GE', 'Georgia'),
('DE', 'Germany'),
('GH', 'Ghana'),
('GI', 'Gibraltar'),
('GR', 'Greece'),
('GL', 'Greenland'),
('GD', 'Grenada'),
('GP', 'Guadeloupe'),
('GU', 'Guam'),
('GT', 'Guatemala'),
('GG', 'Guernsey'),
('GN', 'Guinea'),
('GW', 'Guinea-Bissau'),
('GY', 'Guyana'),
('HT', 'Haiti'),
('HM', 'Heard Island and McDonald Islands'),
('VA', 'Holy See (the)'),
('HN', 'Honduras'),
('HK', 'Hong Kong'),
('HU', 'Hungary'),
('IS', 'Iceland'),
('IN', 'India'),
('ID', 'Indonesia'),
('IR', 'Iran (Islamic Republic of)'),
('IQ', 'Iraq'),
('IE', 'Ireland'),
('IM', 'Isle of Man'),
('IL', 'Israel'),
('IT', 'Italy'),
('JM', 'Jamaica'),
('JP', 'Japan'),
('JE', 'Jersey'),
('JO', 'Jordan'),
('KZ', 'Kazakhstan'),
('KE', 'Kenya'),
('KI', 'Kiribati'),
('KP', 'Korea (the Democratic People''s Republic of)'),
('KR', 'Korea (the Republic of)'),
('KW', 'Kuwait'),
('KG', 'Kyrgyzstan'),
('LA', 'Lao People''s Democratic Republic (the)'),
('LV', 'Latvia'),
('LB', 'Lebanon'),
('LS', 'Lesotho'),
('LR', 'Liberia'),
('LY', 'Libya'),
('LI', 'Liechtenstein'),
('LT', 'Lithuania'),
('LU', 'Luxembourg'),
('MO', 'Macao'),
('MG', 'Madagascar'),
('MW', 'Malawi'),
('MY', 'Malaysia'),
('MV', 'Maldives'),
('ML', 'Mali'),
('MT', 'Malta'),
('MH', 'Marshall Islands (the)'),
('MQ', 'Martinique'),
('MR', 'Mauritania'),
('MU', 'Mauritius'),
('YT', 'Mayotte'),
('MX', 'Mexico'),
('FM', 'Micronesia (Federated States of)'),
('MD', 'Moldova (the Republic of)'),
('MC', 'Monaco'),
('MN', 'Mongolia'),
('ME', 'Montenegro'),
('MS', 'Montserrat'),
('MA', 'Morocco'),
('MZ', 'Mozambique'),
('MM', 'Myanmar'),
('NA', 'Namibia'),
('NR', 'Nauru'),
('NP', 'Nepal'),
('NL', 'Netherlands (the)'),
('NC', 'New Caledonia'),
('NZ', 'New Zealand'),
('NI', 'Nicaragua'),
('NE', 'Niger (the)'),
('NG', 'Nigeria'),
('NU', 'Niue'),
('NF', 'Norfolk Island'),
('MP', 'Northern Mariana Islands (the)'),
('NO', 'Norway'),
('OM', 'Oman'),
('PK', 'Pakistan'),
('PW', 'Palau'),
('PS', 'Palestine, State of'),
('PA', 'Panama'),
('PG', 'Papua New Guinea'),
('PY', 'Paraguay'),
('PE', 'Peru'),
('PH', 'Philippines (the)'),
('PN', 'Pitcairn'),
('PL', 'Poland'),
('PT', 'Portugal'),
('PR', 'Puerto Rico'),
('QA', 'Qatar'),
('MK', 'Republic of North Macedonia'),
('RO', 'Romania'),
('RU', 'Russian Federation (the)'),
('RW', 'Rwanda'),
('RE', 'Réunion'),
('BL', 'Saint Barthélemy'),
('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
('KN', 'Saint Kitts and Nevis'),
('LC', 'Saint Lucia'),
('MF', 'Saint Martin (French part)'),
('PM', 'Saint Pierre and Miquelon'),
('VC', 'Saint Vincent and the Grenadines'),
('WS', 'Samoa'),
('SM', 'San Marino'),
('ST', 'Sao Tome and Principe'),
('SA', 'Saudi Arabia'),
('SN', 'Senegal'),
('RS', 'Serbia'),
('SC', 'Seychelles'),
('SL', 'Sierra Leone'),
('SG', 'Singapore'),
('SX', 'Sint Maarten (Dutch part)'),
('SK', 'Slovakia'),
('SI', 'Slovenia'),
('SB', 'Solomon Islands'),
('SO', 'Somalia'),
('ZA', 'South Africa'),
('GS', 'South Georgia and the South Sandwich Islands'),
('SS', 'South Sudan'),
('ES', 'Spain'),
('LK', 'Sri Lanka'),
('SD', 'Sudan (the)'),
('SR', 'Suriname'),
('SJ', 'Svalbard and Jan Mayen'),
('SE', 'Sweden'),
('CH', 'Switzerland'),
('SY', 'Syrian Arab Republic'),
('TW', 'Taiwan (Province of China)'),
('TJ', 'Tajikistan'),
('TZ', 'Tanzania, United Republic of'),
('TH', 'Thailand'),
('TL', 'Timor-Leste'),
('TG', 'Togo'),
('TK', 'Tokelau'),
('TO', 'Tonga'),
('TT', 'Trinidad and Tobago'),
('TN', 'Tunisia'),
('TR', 'Turkey'),
('TM', 'Turkmenistan'),
('TC', 'Turks and Caicos Islands (the)'),
('TV', 'Tuvalu'),
('UG', 'Uganda'),
('UA', 'Ukraine'),
('AE', 'United Arab Emirates (the)'),
('GB', 'United Kingdom of Great Britain and Northern Ireland (the)'),
('UM', 'United States Minor Outlying Islands (the)'),
('US', 'United States of America (the)'),
('UY', 'Uruguay'),
('UZ', 'Uzbekistan'),
('VU', 'Vanuatu'),
('VE', 'Venezuela (Bolivarian Republic of)'),
('VN', 'Viet Nam'),
('VG', 'Virgin Islands (British)'),
('VI', 'Virgin Islands (U.S.)'),
('WF', 'Wallis and Futuna'),
('EH', 'Western Sahara'),
('YE', 'Yemen'),
('ZM', 'Zambia'),
('ZW', 'Zimbabwe'),
('AX', 'Åland Islands');

UPDATE public.countries
SET risk_tier = 'Low', is_sanctioned = FALSE;
UPDATE public.countries
SET risk_tier = 'High', is_sanctioned = TRUE
WHERE code IN ('IR', 'KP', 'MM');
UPDATE public.countries
SET risk_tier = 'Medium', is_sanctioned = FALSE
WHERE code IN (
  'DZ', 'AO', 'BO', 'BG', 'BF', 'CM', 'CI', 'CD', 'HT', 'KE',
  'LA', 'LB', 'MG', 'ML', 'MN', 'MZ', 'NA', 'NG', 'NI', 'PH',
  'SN', 'ZA', 'SS', 'SY', 'TZ', 'VE', 'VN', 'CM', 'CR'
);

-- =====================================================
-- 3️⃣ CURRENCY
-- =====================================================
DROP TABLE IF EXISTS public.currency CASCADE;
CREATE TABLE public.currency (
  code CHAR(3) PRIMARY KEY,
  name TEXT,
  country_code CHAR(2) REFERENCES public.countries(code),
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.currency (code, name, country_code)
VALUES
('AUD', 'Australian Dollar', 'AU'),
('CAD', 'Canadian Dollar', 'CA'),
('CHF', 'Swiss Franc', 'CH'),
('CNY', 'Chinese Yuan', 'CN'),
('EUR', 'Euro', 'NL'),
('GBP', 'British Pound Sterling', 'GB'),
('HKD', 'Hong Kong Dollar', 'HK'),
('JPY', 'Japanese Yen', 'JP'),
('NZD', 'New Zealand Dollar', 'NZ'),
('SGD', 'Singapore Dollar', 'SG'),
('USD', 'United States Dollar', 'US');

-- =====================================================
-- 4️⃣ TENANTS
-- =====================================================
DROP TABLE IF EXISTS public.tenants CASCADE;
CREATE TABLE public.tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_code TEXT UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.tenants (tenant_code, name)
VALUES
('SG', 'Singapore'),
('MY', 'Malaysia'),
('ID', 'Indonesia'),
('TH', 'Thailand'),
('VN', 'Vietnam'),
('PH', 'Philippines'),
('MM', 'Myanmar'),
('HK', 'Hong Kong'),
('CN', 'China'),
('JP', 'Japan'),
('KR', 'South Korea'),
('TW', 'Taiwan'),
('AU', 'Australia'),
('NZ', 'New Zealand');

-- =====================================================
-- 5️⃣ RULES
-- =====================================================
DROP TABLE IF EXISTS public.rules CASCADE;
CREATE TABLE public.rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_code TEXT UNIQUE NOT NULL,
  rule_name TEXT,
  description TEXT,
  threshold JSONB,
  transaction_type TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.rules (rule_code, rule_name, description, threshold, transaction_type)
VALUES
('AML-TRX-ALL-A-01', 'High-Value Transaction',
 'Transaction Amount is greater than $100K',
 '{"amount_gt": 100000}', 'TRANSFER'),
('AML-TRX-ALL-B-02', 'Transaction to Sanctioned Country',
 'Transaction made to any sanctioned country (from countries table)',
 '{"is_sanctioned": true}', 'TRANSFER'),
('AML-ATM-ALL-C-03', 'ATM 3-Day Withdrawal Pattern',
 '3 ATM withdrawals made in 3 consecutive days with transaction amount more than $5K',
 '{"min_withdrawals": 3, "period_days": 3, "amount_gt": 5000}', 'ATM'),
('AML-XFER-ALL-D-04', 'Frequent Low-Value Transfers',
 'Money sent 10 times to the same country where amount is less than $100',
 '{"count": 10, "amount_lt": 100}', 'TRANSFER');

-- =====================================================
-- 6️⃣ RULES ↔ TENANTS MAPPING
-- =====================================================
DROP TABLE IF EXISTS public.rulestenants CASCADE;
CREATE TABLE public.rulestenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_id UUID REFERENCES public.rules(id),
  tenant_id UUID REFERENCES public.tenants(id),
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.rulestenants (rule_id, tenant_id, created_at)
SELECT r.id, t.id, NOW()
FROM public.rules r
CROSS JOIN public.tenants t;