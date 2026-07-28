const QUIZ_DATA = {
  'bst-1': {
    title: 'Business, Trade and Commerce',
    questions: [
      {
        q: 'Which of the following is NOT a characteristic of business?',
        options: [
          'Production or exchange of goods and services',
          'One-time transaction',
          'Regularity of dealings',
          'Risk and uncertainty'
        ],
        correct: 1,
        explanation: 'Business involves regularity of dealings. A one-time transaction (e.g., selling an old car) is not considered business.'
      },
      {
        q: 'What is a "Darshani Hundi"?',
        options: [
          'A hundi payable on demand',
          'A hundi payable after a specified time period',
          'A hundi drawn by one merchant on another',
          'A hundi that cannot be transferred'
        ],
        correct: 0,
        explanation: 'Darshani Hundi is payable on sight/demand by the drawee, whereas Muddati Hundi is payable after a specified time period.'
      },
      {
        q: 'Which of the following is a tertiary industry?',
        options: [
          'Mining',
          'Fishing',
          'Banking',
          'Manufacturing'
        ],
        correct: 2,
        explanation: 'Tertiary industries provide services. Banking, insurance, and transport are tertiary. Mining and fishing are primary, manufacturing is secondary.'
      },
      {
        q: 'Which of the following is NOT an auxiliary to commerce?',
        options: [
          'Banking',
          'Insurance',
          'Manufacturing',
          'Advertising'
        ],
        correct: 2,
        explanation: 'Manufacturing is an industry (secondary sector), not an auxiliary to commerce. Auxiliaries include banking, insurance, transport, warehousing, and advertising.'
      },
      {
        q: 'Business risk arises due to which of the following reasons?',
        options: [
          'Uncertainties of profit',
          'Changes in government policies',
          'Natural calamities',
          'All of the above'
        ],
        correct: 3,
        explanation: 'Business risk arises from various sources including profit uncertainties, policy changes, natural disasters, theft, and market fluctuations.'
      }
    ]
  },

  'bst-2': {
    title: 'Forms of Business Organisation',
    questions: [
      {
        q: 'What is the maximum number of members allowed in a private company as per the Companies Act, 2013?',
        options: [
          '50',
          '100',
          '200',
          'No limit'
        ],
        correct: 2,
        explanation: 'A private company cannot have more than 200 members (excluding past and present employees who are also members), as per Section 2(68) of the Companies Act, 2013.'
      },
      {
        q: 'In a Joint Hindu Family business, the head of the family is called:',
        options: [
          'Karta',
          'Coparcener',
          'Manager',
          'Owner'
        ],
        correct: 0,
        explanation: 'The Karta is the senior male member who manages the Joint Hindu Family business. Other male members are called coparceners.'
      },
      {
        q: 'Which form of business organisation is best suited for small businesses requiring limited capital and individual control?',
        options: [
          'Joint Hindu Family',
          'Sole Proprietorship',
          'Cooperative Society',
          'Joint Stock Company'
        ],
        correct: 1,
        explanation: 'Sole proprietorship is suitable for small operations with limited capital as the owner has complete control and minimal legal formalities.'
      },
      {
        q: 'In a cooperative society, the liability of members is:',
        options: [
          'Unlimited',
          'Limited to their share capital',
          'Joint and several',
          'Limited to personal assets'
        ],
        correct: 1,
        explanation: 'The liability of members in a cooperative society is limited to the extent of their share capital. Members are not personally liable for the society\'s debts.'
      },
      {
        q: 'What is the maximum number of partners permitted in a partnership firm carrying on banking business?',
        options: [
          '10',
          '20',
          '50',
          '100'
        ],
        correct: 0,
        explanation: 'As per the Indian Partnership Act, 1932, the maximum number of partners is 10 for banking business and 20 for other businesses.'
      }
    ]
  },

  'bst-3': {
    title: 'Private, Public and Global Enterprises',
    questions: [
      {
        q: 'A government company is one in which the government holds at least what percentage of paid-up share capital?',
        options: [
          '25%',
          '50%',
          '51%',
          '74%'
        ],
        correct: 2,
        explanation: 'A government company is defined under Section 2(45) of the Companies Act, 2013 as a company in which at least 51% of the paid-up share capital is held by the government.'
      },
      {
        q: 'Which of the following is NOT a characteristic of public sector enterprises?',
        options: [
          'Government ownership',
          'Profit maximisation as the sole objective',
          'Public accountability',
          'Social welfare orientation'
        ],
        correct: 1,
        explanation: 'Public sector enterprises focus on social welfare and public service along with profitability. Profit maximisation is not their sole objective.'
      },
      {
        q: 'A joint venture involves:',
        options: [
          'Two or more firms pooling resources for a specific project',
          'A government taking over a private company',
          'A company issuing shares to the public',
          'One firm acquiring another firm'
        ],
        correct: 0,
        explanation: 'A joint venture is a business arrangement where two or more firms pool their resources, capital, and expertise to undertake a specific project or business activity.'
      },
      {
        q: 'PPP stands for:',
        options: [
          'Public-Private Partnership',
          'Private-Public Procurement',
          'Public Purchase Program',
          'Private Property Plan'
        ],
        correct: 0,
        explanation: 'PPP or Public-Private Partnership is a model where the government partners with private sector companies to deliver public services and infrastructure projects.'
      },
      {
        q: 'Which of the following is an example of a statutory corporation?',
        options: [
          'Bharat Heavy Electricals Limited (BHEL)',
          'Life Insurance Corporation of India (LIC)',
          'Hindustan Machine Tools (HMT)',
          'Indian Oil Corporation (IOC)'
        ],
        correct: 1,
        explanation: 'LIC is a statutory corporation established by a special Act of Parliament (LIC Act, 1956). BHEL, HMT, and IOC are government companies registered under the Companies Act.'
      }
    ]
  },

  'bst-4': {
    title: 'Business Services',
    questions: [
      {
        q: 'Which type of bank provides long-term finance to industries?',
        options: [
          'Commercial bank',
          'Development bank',
          'Cooperative bank',
          'Central bank'
        ],
        correct: 1,
        explanation: 'Development banks (e.g., IDBI, SIDBI) provide long-term industrial finance. Commercial banks primarily offer short-term credit and working capital.'
      },
      {
        q: 'The principle of indemnity applies to which type of insurance?',
        options: [
          'Life insurance only',
          'Fire insurance only',
          'Marine insurance only',
          'Both fire and marine insurance'
        ],
        correct: 3,
        explanation: 'Fire and marine insurance are contracts of indemnity — they compensate the actual loss. Life insurance is not a contract of indemnity since human life cannot be valued.'
      },
      {
        q: 'Which mode of transport is most suitable for transporting bulky and heavy goods over long distances across land?',
        options: [
          'Road transport',
          'Railway transport',
          'Air transport',
          'Water transport'
        ],
        correct: 1,
        explanation: 'Railways are ideal for carrying bulky, heavy goods over long distances at relatively low cost. Road transport suits short distances, air is for perishable/valuable items.'
      },
      {
        q: 'Warehousing provides which type of utility?',
        options: [
          'Form utility',
          'Place utility',
          'Time utility',
          'Possession utility'
        ],
        correct: 2,
        explanation: 'Warehousing creates time utility by storing goods when they are produced and making them available when needed. Place utility is created by transport, form by manufacturing.'
      },
      {
        q: 'Which of the following is NOT a means of communication?',
        options: [
          'Mobile phone',
          'Courier service',
          'Warehouse',
          'Internet'
        ],
        correct: 2,
        explanation: 'A warehouse is used for storage of goods, not communication. Mobile phones, courier services, and the internet are all means of communication.'
      }
    ]
  },

  'eco-1': {
    title: 'Introduction to Microeconomics',
    questions: [
      {
        q: 'The central problems of an economy arise due to:',
        options: [
          'Scarcity of resources alone',
          'Unlimited human wants alone',
          'Both scarcity of resources and unlimited human wants',
          'Abundance of resources'
        ],
        correct: 2,
        explanation: 'Central problems (what, how, and for whom to produce) arise because resources are scarce but human wants are unlimited, forcing choices.'
      },
      {
        q: 'The Production Possibility Frontier (PPF) is concave to the origin because of:',
        options: [
          'Increasing Marginal Opportunity Cost',
          'Decreasing Marginal Opportunity Cost',
          'Constant Marginal Opportunity Cost',
          'Zero Marginal Opportunity Cost'
        ],
        correct: 0,
        explanation: 'The PPF is concave because resources are not equally efficient in producing all goods. As more of one good is produced, the marginal opportunity cost rises.'
      },
      {
        q: 'What does a point inside the Production Possibility Frontier indicate?',
        options: [
          'Efficient utilisation of resources',
          'Underutilisation of resources',
          'Unattainable level of production',
          'Full employment of resources'
        ],
        correct: 1,
        explanation: 'Points inside the PPF show underutilisation of resources (unemployment or inefficiency). Points on the PPF represent efficient production. Points beyond are unattainable.'
      },
      {
        q: 'Opportunity cost of producing a good is:',
        options: [
          'The total cost of production',
          'The cost of the next best alternative foregone',
          'The money spent on inputs',
          'The market price of the good'
        ],
        correct: 1,
        explanation: 'Opportunity cost is the value of the next best alternative that must be given up to produce or obtain something else.'
      },
      {
        q: 'Which of the following is NOT one of the three central problems of an economy?',
        options: [
          'What to produce',
          'How to produce',
          'When to produce',
          'For whom to produce'
        ],
        correct: 2,
        explanation: 'The three central problems are: what to produce, how to produce, and for whom to produce. "When to produce" is not a central problem.'
      }
    ]
  },

  'eco-2': {
    title: "Consumer's Equilibrium",
    questions: [
      {
        q: 'Total Utility is maximum when Marginal Utility is:',
        options: [
          'Positive',
          'Zero',
          'Negative',
          'Constant'
        ],
        correct: 1,
        explanation: 'According to the law of diminishing marginal utility, TU is maximum when MU becomes zero. Beyond this point, MU becomes negative and TU starts declining.'
      },
      {
        q: 'An indifference curve is:',
        options: [
          'Concave to the origin',
          'Convex to the origin',
          'Upward sloping',
          'A vertical straight line'
        ],
        correct: 1,
        explanation: 'Indifference curves are convex to the origin due to the diminishing marginal rate of substitution (MRS).'
      },
      {
        q: 'The slope of the budget line is equal to:',
        options: [
          'MUx / MUy',
          'Px / Py',
          'Py / Px',
          'MRSxy'
        ],
        correct: 1,
        explanation: 'The slope of the budget line is the ratio of prices of the two goods (Px/Py), representing the rate at which the market allows substitution of one good for another.'
      },
      {
        q: 'In the case of a single commodity, a consumer is in equilibrium when:',
        options: [
          'MUx = Px',
          'MUx > Px',
          'MUx < Px',
          'TUx = Px'
        ],
        correct: 0,
        explanation: 'For a single commodity, consumer equilibrium occurs where Marginal Utility equals Price (MUx = Px). If MU > P, the consumer buys more; if MU < P, the consumer buys less.'
      },
      {
        q: 'Which of the following assumptions is NOT required for the indifference curve analysis?',
        options: [
          'Rational consumer',
          'Ordinal utility',
          'Cardinal utility',
          'Diminishing marginal rate of substitution'
        ],
        correct: 2,
        explanation: 'Indifference curve analysis assumes ordinal utility (ranking), not cardinal utility (measurable numbers). It only requires that consumers can rank their preferences.'
      }
    ]
  },

  'eco-3': {
    title: 'Demand',
    questions: [
      {
        q: 'The Law of Demand states that, other things remaining constant:',
        options: [
          'Price and quantity demanded are directly related',
          'Price and quantity demanded are inversely related',
          'Demand increases when income increases',
          'Supply increases when price increases'
        ],
        correct: 1,
        explanation: 'The Law of Demand states that as price rises, quantity demanded falls, and vice versa, assuming other factors remain constant (ceteris paribus).'
      },
      {
        q: 'Contraction of demand occurs when:',
        options: [
          'Price of the good falls',
          'Price of the good rises',
          'Income of the consumer rises',
          'Income of the consumer falls'
        ],
        correct: 1,
        explanation: 'Contraction of demand refers to a fall in quantity demanded due to a rise in the price of the good, with other factors unchanged.'
      },
      {
        q: 'Which of the following is an exception to the Law of Demand?',
        options: [
          'Normal goods',
          'Giffen goods',
          'Luxury goods',
          'Inferior goods'
        ],
        correct: 1,
        explanation: 'Giffen goods violate the Law of Demand — their demand rises when price rises and falls when price falls. They are a special type of inferior goods with a strong income effect.'
      },
      {
        q: 'When the price of a substitute good rises, the demand for the given good:',
        options: [
          'Falls',
          'Rises',
          'Remains unchanged',
          'Becomes zero'
        ],
        correct: 1,
        explanation: 'Substitute goods (e.g., tea and coffee) are consumed in place of each other. If the price of one rises, consumers shift to the other, increasing its demand.'
      },
      {
        q: 'Giffen goods are a special type of:',
        options: [
          'Normal goods',
          'Luxury goods',
          'Inferior goods',
          'Veblen goods'
        ],
        correct: 2,
        explanation: 'Giffen goods are a specific category of inferior goods that have no close substitutes and for which the income effect outweighs the substitution effect.'
      }
    ]
  },

  'eco-4': {
    title: 'Elasticity of Demand',
    questions: [
      {
        q: 'Price elasticity of demand is defined as:',
        options: [
          'Percentage change in quantity demanded divided by percentage change in price',
          'Change in quantity demanded divided by change in price',
          'Percentage change in price divided by percentage change in quantity demanded',
          'Total expenditure divided by total quantity'
        ],
        correct: 0,
        explanation: 'Price elasticity measures responsiveness of quantity demanded to price changes. It is the ratio of percentage change in quantity demanded to percentage change in price.'
      },
      {
        q: 'When demand is perfectly inelastic, the value of price elasticity is:',
        options: [
          '1',
          '0',
          'Infinity',
          'Greater than 1'
        ],
        correct: 1,
        explanation: 'Perfectly inelastic demand (Ed = 0) means quantity demanded does not change at all when price changes. The demand curve is a vertical straight line.'
      },
      {
        q: 'Which method of measuring price elasticity uses the formula Ed = (ΔQ/ΔP) × (P/Q)?',
        options: [
          'Percentage method',
          'Geometric method',
          'Total expenditure method',
          'Revenue method'
        ],
        correct: 0,
        explanation: 'The percentage method (or proportionate method) calculates elasticity as (percentage change in Qd) / (percentage change in P), which simplifies to (ΔQ/ΔP) × (P/Q).'
      },
      {
        q: 'A commodity with a large number of close substitutes will have:',
        options: [
          'Low price elasticity',
          'High price elasticity',
          'Zero price elasticity',
          'Unitary price elasticity'
        ],
        correct: 1,
        explanation: 'Goods with many close substitutes (like a specific brand of soap) have high price elasticity because consumers can easily switch when price changes.'
      },
      {
        q: 'If total expenditure on a commodity remains unchanged when price changes, the elasticity of demand is:',
        options: [
          'Greater than 1',
          'Less than 1',
          'Equal to 1',
          'Zero'
        ],
        correct: 2,
        explanation: 'Under the total expenditure method, if TE remains constant when price changes, demand has unitary elasticity (Ed = 1).'
      }
    ]
  },

  'stat-1': {
    title: 'Economics — An Introduction',
    questions: [
      {
        q: 'Who defined Economics as "the science of wealth"?',
        options: [
          'Adam Smith',
          'Alfred Marshall',
          'Lionel Robbins',
          'Paul Samuelson'
        ],
        correct: 0,
        explanation: 'Adam Smith, in his book "An Inquiry into the Nature and Causes of the Wealth of Nations" (1776), defined economics as the science of wealth.'
      },
      {
        q: 'Which of the following is an economic activity?',
        options: [
          'A mother cooking for her family',
          'A teacher teaching in a school for salary',
          'A person gardening as a hobby',
          'A friend helping another with homework'
        ],
        correct: 1,
        explanation: 'An economic activity involves monetary remuneration. The teacher receives a salary, making it economic. The other options are non-economic activities done out of love or hobby.'
      },
      {
        q: 'The problem of scarcity arises because:',
        options: [
          'Resources are unlimited and wants are limited',
          'Resources are limited and wants are unlimited',
          'Both resources and wants are unlimited',
          'Both resources and wants are limited'
        ],
        correct: 1,
        explanation: 'Scarcity is the fundamental economic problem — human wants are unlimited but the resources to satisfy them are limited, forcing choices.'
      },
      {
        q: '"Economics is the science of choice" — this definition is associated with:',
        options: [
          'Adam Smith',
          'Alfred Marshall',
          'Lionel Robbins',
          'J.M. Keynes'
        ],
        correct: 2,
        explanation: 'Lionel Robbins defined economics as "the science of choice" in his book "An Essay on the Nature and Significance of Economic Science" (1932), based on scarcity.'
      },
      {
        q: 'Which of the following statements is an example of normative economics?',
        options: [
          'Unemployment in India is 6%',
          'India should reduce income inequality',
          'Inflation rate rose by 2% this year',
          'GDP growth rate is 7%'
        ],
        correct: 1,
        explanation: 'Normative economics involves value judgments about what ought to be. "India should reduce income inequality" is a normative statement, while the others are factual (positive).'
      }
    ]
  },

  'stat-2': {
    title: 'Meaning, Scope & Importance of Statistics',
    questions: [
      {
        q: 'In the singular sense, the word "Statistics" refers to:',
        options: [
          'Numerical data',
          'Statistical methods',
          'Collection of numerical facts',
          'Plural of the word statistic'
        ],
        correct: 1,
        explanation: 'In the singular sense, Statistics refers to the science of statistical methods — the techniques used to collect, analyse, and interpret data.'
      },
      {
        q: 'According to Bowley, Statistics is described as the "science of":',
        options: [
          'Wealth',
          'Averages',
          'Choice',
          'Numbers'
        ],
        correct: 1,
        explanation: 'Bowley described Statistics as "the science of counting and averages." This highlights that statistics deals with aggregate data and summary measures.'
      },
      {
        q: 'Which of the following is a function of statistics?',
        options: [
          'Simplification of complex data',
          'Comparison of data',
          'Forecasting',
          'All of the above'
        ],
        correct: 3,
        explanation: 'Statistics serves multiple functions: presenting complex data simply, enabling comparison, aiding forecasting, and formulating policies.'
      },
      {
        q: 'Statistics does NOT study:',
        options: [
          'Qualitative phenomena',
          'Quantitative phenomena',
          'Aggregate data',
          'Numerical facts'
        ],
        correct: 0,
        explanation: 'Statistics deals only with quantitative (numerical) data. It does not study qualitative phenomena like honesty, beauty, or intelligence unless they are quantified.'
      },
      {
        q: '"Statistics are the eyes of administration" — this statement is attributed to:',
        options: [
          'Bowley',
          'Tippett',
          'W.I. King',
          'Croxton and Cowden'
        ],
        correct: 2,
        explanation: 'W.I. King emphasised the importance of statistics in governance by stating that "Statistics are the eyes of administration."'
      }
    ]
  },

  'stat-3': {
    title: 'Collection of Data',
    questions: [
      {
        q: 'Primary data is collected by the investigator:',
        options: [
          'For the first time for a specific purpose',
          'From already published sources',
          'From government records',
          'From newspapers and journals'
        ],
        correct: 0,
        explanation: 'Primary data is original data collected for the first time by the investigator for a specific purpose. It is first-hand and not previously published.'
      },
      {
        q: 'Which of the following is a method of collecting primary data?',
        options: [
          'Direct personal interview',
          'Published government reports',
          'Newspapers',
          'Journals'
        ],
        correct: 0,
        explanation: 'Direct personal interview is a primary data collection method where the investigator personally meets respondents. Published reports and newspapers provide secondary data.'
      },
      {
        q: 'A census survey covers:',
        options: [
          'A selected sample of the population',
          'Each and every unit of the population',
          'Only urban areas',
          'Only rural areas'
        ],
        correct: 1,
        explanation: 'Census (or complete enumeration) covers every single unit of the population. It provides comprehensive data but is costly and time-consuming.'
      },
      {
        q: 'In random sampling:',
        options: [
          'Every item has an equal chance of being selected',
          'Items are selected deliberately by the investigator',
          'Only conveniently available items are selected',
          'Items are selected from only one group'
        ],
        correct: 0,
        explanation: 'Random sampling gives every item in the population an equal and independent chance of being selected, eliminating investigator bias.'
      },
      {
        q: 'Which of the following is a limitation of secondary data?',
        options: [
          'It is always reliable',
          'It may not suit the current objective',
          'It is very expensive to collect',
          'It takes a lot of time'
        ],
        correct: 1,
        explanation: 'A key limitation of secondary data is that it was collected for a different purpose and may not be suitable for the current research objective.'
      }
    ]
  },

  'stat-4': {
    title: 'Organisation of Data',
    questions: [
      {
        q: 'Classification of data refers to:',
        options: [
          'Arranging data in rows and columns',
          'Grouping data according to similarities',
          'Drawing graphs from data',
          'Calculating averages'
        ],
        correct: 1,
        explanation: 'Classification is the process of arranging data into groups or classes based on common characteristics or similarities.'
      },
      {
        q: 'A frequency distribution shows:',
        options: [
          'The number of observations in each class',
          'Only the class intervals',
          'Only the total number of classes',
          'The mid-point of each class'
        ],
        correct: 0,
        explanation: 'A frequency distribution organises data into classes and shows the frequency (number of observations) falling into each class.'
      },
      {
        q: 'In a frequency distribution, the class midpoint is calculated as:',
        options: [
          'Upper limit − Lower limit',
          '(Upper limit + Lower limit) / 2',
          '(Upper limit − Lower limit) / 2',
          'Upper limit × Lower limit'
        ],
        correct: 1,
        explanation: 'The class midpoint (or mid-value) is the average of the upper and lower limits of a class interval: (Upper limit + Lower limit) / 2.'
      },
      {
        q: 'Continuous variables can take:',
        options: [
          'Only integer values',
          'Any value within a given range',
          'Only two distinct values',
          'Values from a set of fixed numbers'
        ],
        correct: 1,
        explanation: 'Continuous variables can take any numerical value within a range (e.g., height, weight, temperature). They are not restricted to integers.'
      },
      {
        q: 'Which type of classification arranges data on the basis of time periods?',
        options: [
          'Qualitative classification',
          'Quantitative classification',
          'Chronological classification',
          'Geographical classification'
        ],
        correct: 2,
        explanation: 'Chronological (or temporal) classification organises data according to time periods such as years, months, or days.'
      }
    ]
  },

  'stat-5': {
    title: 'Tabular Presentation',
    questions: [
      {
        q: 'The horizontal arrangement of data in a table is called a:',
        options: [
          'Column',
          'Row',
          'Caption',
          'Stub'
        ],
        correct: 1,
        explanation: 'Rows are the horizontal arrangements in a table. Caption refers to column headings, and stub refers to row headings.'
      },
      {
        q: 'The title of a table should be:',
        options: [
          'Long and highly detailed',
          'Self-explanatory and brief',
          'Written in capital letters only',
          'Placed at the bottom of the table'
        ],
        correct: 1,
        explanation: 'A good table title should be concise yet self-explanatory, clearly indicating the content, time period, and location of the data.'
      },
      {
        q: 'The part of a table that describes the column headings is called the:',
        options: [
          'Stub',
          'Caption',
          'Body',
          'Headnote'
        ],
        correct: 1,
        explanation: 'The caption is the part of the table that contains column headings (what each column represents). The stub contains row headings.'
      },
      {
        q: 'Tabulation is the process of:',
        options: [
          'Classifying data into groups',
          'Presenting data in rows and columns',
          'Collecting data from the field',
          'Analysing data using formulas'
        ],
        correct: 1,
        explanation: 'Tabulation is the process of presenting data systematically in rows and columns. Classification precedes tabulation.'
      },
      {
        q: 'A table that shows how many observations fall into each class is called a:',
        options: [
          'Simple table',
          'Complex table',
          'Frequency distribution table',
          'Reference table'
        ],
        correct: 2,
        explanation: 'A frequency distribution table organises data into classes and shows the frequency (count) of observations in each class.'
      }
    ]
  }
};
