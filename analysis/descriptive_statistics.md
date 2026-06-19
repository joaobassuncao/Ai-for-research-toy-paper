# Descriptive statistics — Stack Overflow Annual Developer Survey

Generated from `data/results.csv` (49,191 respondents x 172 columns). The CSV
itself is not committed to this repo (see `data/README.md` for the license
and the download script); these numbers are the durable record of what was
in it.

Key variables used:

| Concept | Column(s) |
|---|---|
| AI-tool use | `AISelect` |
| Job satisfaction | `JobSat` (0-10 derived score) |
| Years of pro experience | `WorkExp`, `YearsCode` |
| Developer role | `DevType` |

## Missingness on key variables

| Column | % missing |
|---|---|
| AISelect | 31.5% |
| JobSat | 45.8% |
| YearsCode | 12.5% |
| WorkExp | 12.8% |
| DevType | 11.2% |

Complete-case N across all four key variables: **24,354 of 49,191 (49.5%)**.

## AISelect distribution

| Response | n | % of total |
|---|---|---|
| Yes, daily | 15,883 | 32.3% |
| Yes, weekly | 5,958 | 12.1% |
| Yes, monthly/infrequent | 4,628 | 9.4% |
| No, plan to soon | 1,797 | 3.7% |
| No, don't plan to | 5,454 | 11.1% |
| Missing | 15,471 | 31.5% |

## Job satisfaction (JobSat, 0-10)

n = 26,670; mean 7.20; sd 2.00; median 8; IQR [6, 8]; range [0, 10].

### JobSat by AISelect

| AI-tool use | n | mean | median | sd |
|---|---|---|---|---|
| Yes, daily | 12,599 | 7.29 | 8 | 1.96 |
| Yes, weekly | 4,353 | 7.14 | 7 | 1.89 |
| Yes, monthly/infrequent | 3,188 | 7.11 | 7 | 2.02 |
| No, plan to soon | 1,135 | 7.11 | 8 | 2.08 |
| No, don't plan to | 3,643 | 7.14 | 8 | 2.12 |

### JobSat by DevType (top 10 roles by n)

| DevType | n | mean | median | sd |
|---|---|---|---|---|
| Full-stack | 9,385 | 7.20 | 8 | 1.98 |
| Back-end | 4,937 | 7.04 | 7 | 1.98 |
| Architect | 1,865 | 7.54 | 8 | 1.88 |
| Desktop/enterprise | 1,454 | 7.21 | 8 | 1.97 |
| Front-end | 1,418 | 6.98 | 7 | 2.03 |
| Mobile | 1,029 | 7.21 | 8 | 2.00 |
| Embedded | 962 | 7.13 | 7 | 2.00 |
| Other | 502 | 7.08 | 8 | 2.52 |
| Student | 355 | 6.85 | 7 | 2.12 |
| Academic researcher | 285 | 7.36 | 8 | 1.89 |

## Years of professional experience (WorkExp, years)

n = 42,893; mean 13.4; sd 10.8; median 10; IQR [5, 20]; range [1, 100]
(max is almost certainly a top-coded/cleaning artifact).

### WorkExp by AISelect

| AI-tool use | n | mean | median |
|---|---|---|---|
| Yes, daily | 14,880 | 12.8 | 10 |
| Yes, weekly | 5,478 | 13.5 | 11 |
| Yes, monthly/infrequent | 4,220 | 14.8 | 12 |
| No, plan to soon | 1,655 | 18.5 | 16 |
| No, don't plan to | 4,889 | 16.2 | 13 |

AI adoption is skewed toward less-tenured developers: daily users average
~13 years vs. ~16-18 years among non-adopters. This is a confound for any
causal-sounding reading of the AISelect/JobSat relationship.

## Compensation (ConvertedCompYearly, USD)

n = 23,947 (51.3% missing); mean $101,762; median $75,320; sd $461,757;
range $1-$50,000,000. Heavily right-skewed with extreme outliers; prefer
the median.

## Correlations (pairwise, numeric)

| Pair | r |
|---|---|
| JobSat ~ WorkExp | 0.106 |
| JobSat ~ ConvertedCompYearly | 0.024 |
| WorkExp ~ ConvertedCompYearly | 0.054 |

All weak. Job satisfaction is essentially uncorrelated with both tenure and
pay in this raw cross-section.

## Sample composition

Country (top 5): USA 7,233; Germany 3,025; India 2,547; UK 2,042; France 1,409.

RemoteWork: Remote 10,931; Hybrid (in-person-leaning) 6,732; In-person 6,042;
Hybrid (flexible-leaning) 5,831; fully flexible 4,244; missing 15,411 (31.3%).

## Reproducing

```bash
bash data/download.sh        # fetches results.csv (not committed, ~140MB)
pip install pandas numpy
python analysis/explore.py
```
