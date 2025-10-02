import os
from typing import List, Dict
import json


# Sample document data - in production, this would be loaded from files or a vector database
SCHOLARSHIP_DOCUMENTS = [
    {
        "id": "doc1",
        "title": "How to Write a Strong Scholarship Essay",
        "content": """
        Writing a compelling scholarship essay is crucial for standing out among applicants. Here are key tips:

        1. Understand the prompt thoroughly before writing
        2. Start with a captivating introduction that hooks the reader
        3. Tell your personal story and highlight your unique qualities
        4. Be specific about your achievements and goals
        5. Connect your experiences to the scholarship's values
        6. Maintain clear structure with introduction, body, and conclusion
        7. Proofread carefully for grammar and spelling errors
        8. Ask for feedback from teachers or mentors
        9. Be authentic and let your passion shine through
        10. Submit before the deadline after multiple revisions

        Remember that scholarship committees read hundreds of essays, so making yours memorable is essential.
        """
    },
    {
        "id": "doc2",
        "title": "Types of Scholarships",
        "content": """
        Scholarships come in various types to support different student needs:

        1. Merit-based scholarships: Awarded based on academic, athletic, or artistic achievements
        2. Need-based scholarships: Given to students with financial need
        3. Career-specific scholarships: For students pursuing particular fields (STEM, healthcare, etc.)
        4. Minority scholarships: Supporting underrepresented groups
        5. Country-specific scholarships: For international students from certain countries
        6. University-specific scholarships: Offered by individual institutions
        7. Government scholarships: Funded by government agencies
        8. Corporate scholarships: Provided by companies and businesses
        9. Athletic scholarships: For students with sports talents
        10. Creative scholarships: For those with artistic abilities

        Understanding these categories helps students target the right opportunities for their profile.
        """
    },
    {
        "id": "doc3",
        "title": "Scholarship Application Timeline",
        "content": """
        Following a strategic timeline improves your chances of scholarship success:

        1. 12-18 months before: Research scholarship opportunities and requirements
        2. 10-12 months before: Prepare standardized test scores if needed
        3. 8-10 months before: Request recommendation letters from professors/teachers
        4. 6-8 months before: Draft and revise your personal statement/essays
        5. 4-6 months before: Gather transcripts and academic records
        6. 3-4 months before: Complete application forms and prepare supporting documents
        7. 2-3 months before: Review all materials for errors and completeness
        8. 1-2 months before: Submit applications (earlier is better)
        9. After submission: Follow up if confirmation isn't received
        10. After decisions: Send thank-you notes regardless of outcome

        Always check individual scholarship deadlines as they vary significantly.
        """
    },
    {
        "id": "doc4",
        "title": "Common Scholarship Application Mistakes",
        "content": """
        Avoid these common mistakes that can hurt your scholarship chances:

        1. Missing deadlines: Late applications are typically rejected immediately
        2. Not following instructions: Failing to provide exactly what's requested
        3. Generic essays: Using the same essay for multiple applications without customization
        4. Poor grammar and spelling: Suggesting carelessness and lack of effort
        5. Lack of proofreading: Submitting without thorough review
        6. Insufficient research: Not understanding the scholarship's purpose and values
        7. Incomplete applications: Missing required documents or information
        8. Exaggerating achievements: Being dishonest about accomplishments
        9. Weak recommendation letters: Choosing recommenders who don't know you well
        10. Ignoring eligibility criteria: Applying for scholarships you don't qualify for

        Taking time to avoid these pitfalls significantly increases your chances of success.
        """
    },
    {
        "id": "doc5",
        "title": "5 Insider Tips and Tricks to Apply for Scholarships",
        "content": """
        1. What Are Scholarships?
Scholarships are an amount of money awarded to students to help them further their education. They’re very different from student loans because they don't have to be paid back. There are many types of scholarships offered for students in high schools, colleges, and universities.

There's also a wide array of scholarship sources, and they could be from the government, universities, corporations, and other organizations of goodwill. One thing you have to understand about scholarships is that they're not exactly free money. You may not have to pay it back, but it will come with some strings attached.

For instance, an athletic scholarship will come with the expectation of performing in a certain sport and maintaining a certain grade point. A scholarship may also be contingent on entering a certain career, so you have to be sure that's the career path you want to pursue before accepting the scholarship. Some scholarships may also expect you to perform certain services in return for getting the scholarship.

2. Types of Scholarships
There are many types of scholarships for almost anything you can think of. You could get a scholarship for making a prom outfit out of duct tape, being a top athlete, or even being left-handed. Scholarship opportunities are almost limitless, and we'll look at some of the most common below:

Athletic Scholarships
Athletic scholarships are for students who excel in sports. Most of these are offered by universities looking to attract top athletes. There are athletic scholarships for all kinds of sports, not just football or basketball, which are two of the most famous.

Some universities offer scholarships for uncommon sports such as water polo, fencing, and even weight lifting. Once you receive the scholarship, you'll have to dedicate yourself to the sport in return.

Merit Scholarships
Merit scholarships are what most people think of when they hear the word scholarships. The scholarships are usually dedicated to the brilliant, dedicated, talented students who look to be the leaders of tomorrow. Merit-based scholarships are some of the best because they offer opportunities to truly talented people who may not have the means to educate themselves.

Community Service Scholarships
Scholarships are usually not reserved for top students only. Those who volunteer in their communities also have a high chance of getting one. Whether you are a US citizen or a legal resident who has already made a positive impact on the community. If you have demonstrated strength and wisdom through volunteer services, you can apply for these.

Need-Based Scholarships
Students with demonstrated financial needs may be able to qualify for a need-based scholarship. Some need-based scholarships may come with specific requirements that pursue particular areas of study or living in a specific community.

Employer or Military Scholarships
You may also be able to get a scholarship through a family member's employer. Some businesses offer scholarships to support the employees' children. Additionally, if you have an active or retired member of the military, you may be able to qualify for the Military Commanders' Scholarship Fund.

3. How to Find the Best Scholarships to Apply for
With the power of the internet, there are so many places for you to find the best scholarships to apply for. There's a wide array of tools and resources available to help you access thousands of scholarships, starting with scholarship websites. Scholarship websites are easily accessible and have thousands of scholarships listed on their platforms.

Most of these websites have easy-to-navigate filter options and search results that will match your individual profile. As expected, there's a lot of competition, and the scholarships may be based on a lottery system. When checking out this website, be wary of scam websites that ask you to pay a fee to apply.

You can also easily find scholarships through search engines by simply typing what kind of scholarship you're looking for. To filter out results, make a list of the category you fit into, such as state, hobbies, gender, sports, GPA, disabilities, etcetera. You can search for stem scholarships, ballet scholarships, scholarships for Arizona students, scholarships for Hispanics, scholarships for women, and the like.

Alternatively, you can check out bulletin boards or newspapers for local scholarships in your community. Check bulletin boards at schools, community centers, churches, or even cafes.

List Your Unique Traits
There are scholarships based on personal interests, nationality, GPA, extracurricular activities, languages spoken, LGBTQ individuals, footballers, pianists, people who grew up with certain hardships, and many more. This means one of the most important things you have to do is create a list of your unique traits so you can narrow down the best scholarships to apply for.

Before you apply for scholarships, list what you're good at, starting with your personal interests or passions and favorite extracurricular activities. Think about your academic accomplishments, personal traits, heritage, gender, and hardships you went through with the past. Once you're done, apply for scholarships based on these traits.

Understand the Application Requirements
Once you find a list of scholarships you want to apply for, it's of absolute importance that you understand the requirements first. Different scholarships will require different documents or the completion of various tasks. Some of the most common documents you may be required include filling out an application form or writing an essay.

Still, some scholarships may require letters of recommendation from professional or personal references. If this is a requirement, ask for letters of recommendation from your professors, teachers, counselors, or personal sources a few weeks in advance. This will give them enough time to reply to you and give you the letter you need.

You may also be required to send copies of transcripts and diplomas. Sometimes, even though you may not be applying for a merit-based scholarship, you may still be required to send your high school diploma or recent school transcripts. You may also find a scholarship application asking for your SAT or ACT scores.

Some of the scholarships may require your financial aid information, especially if you're applying for a need-based scholarship. It may require you to send your parents' income and tax information and submit a FAFSA form. Furthermore, other scholarships may require a resume or a portfolio.

Apply for Scholarships Early
It's never too early to apply for scholarships, and the last thing you want is for deadlines to start sneaking up on you. One of the best things you can do to increase your chances of winning scholarships is to apply for as many scholarships as possible. Starting early will help you manage to send as many as you can, and you could even set a scholarship schedule for yourself.

For instance, you could dedicate 10 scholarships every month, which is about two or three scholarships applications every week. Most of these will take you about 15 minutes to apply, so don't skimp and don't give up. This does not necessarily mean that you should rush your applications.

On the contrary, it's of absolute importance for you to give the necessary time and consideration to every application to be a strong contender. It's important for your application to stand out and reflect your ability to be dedicated and thoughtful in everything you do. Take your time and read all the directions, familiarise yourself with the organization, and make sure you proofread your essay before submission.

Write a Killer Essay
Not every scholarship you apply for will require an essay, but you can expect most of them too. You have to make sure you write the best essay you have ever written. The essay allows you to show a more dimensional aspect of yourself and showcase things that are not reflected on your test scores and GPA.

The first step of rocking the essay is to read the instructions thoroughly and follow them to the letter. If the application requires you to meet a certain word count, then stay within the limit stipulated. If you're required to submit a video or photo with the essay, then make sure you don't overlook any aspect.

Moreover, it's important for you to answer the prompt as clearly and concisely as possible. If you're required to write about your achievement despite certain setbacks, that's exactly what you need to write about.

If you're required to describe how your life will change once you get the scholarship, avoid certain platitudes and cliches. Avoid things like it would mean the world to you or it would be a game-changer. The scholarship organizations already know it would be a game-changer.

What you need to do is describe what life will be like when you get financial assistance. Be as specific as possible and provide the readers with a picture of your aspirations and future goals. Avoid repeating all the things that are on your resume and try to show another layer of who you are as a potential candidate.

When you're done, make sure you proofread and polish your essay. If possible, get someone else to proofread the work for you so they can help you catch any errors you may have missed.  It could be your friend, your parents, or even your teacher.

Submit Your Materials
Now that you have gathered all the required documents, filled out your application form, and written your killer essay, it's time for you to submit everything. Some scholarships will have to be submitted by mail, while others can easily be submitted online.

This will also be in the requirements provided by the organization. If you're required to submit letters of recommendation, make sure your referees know the deadline to avoid any problems.

Keep Checking the Status of Your Scholarship
Once you apply for scholarships and submit all the materials, you need to keep checking the status. Of course, you should also be patient because most organizations will let you know when you can expect feedback.

After you submit your materials, keep a positive attitude as you wait to hear from the providers. It's also imperative for you to have a list of scholarships you have applied for and update it every time you get results. When checking for updates, make sure you check your spam folder as well to avoid having responses go unanswered.

Clean Up Your Social Medial Pages
One of the best things you can do when you apply for scholarships is to clean up your public social media pages. The scholarship organization members will most likely vet their candidates. You want to make sure that your social media pages exude professionalism.

Most scholarships will outright ask for links to your social media profiles. Make sure what they see is exactly what you want to portray about yourself.

4. List of Easy Scholarships to Apply for
Now that you know how to apply for scholarships, there are many easy scholarships you can apply for. Here is a list of easy scholarships you may want to check out:

Because college is expensive scholarship
You deserve it scholarship
Be Bold scholarship
ScholarPoints scholarship
Valentine's day scholarship
DR. Pepper tuition giveaway
AFSA high schools scholarship
5. Don't Give Up
Scholarships can be life-changing, so you must keep the effort and keep applying for more. This is by far one of the most important scholarship tips because the more you apply for, the higher your chances of winning.
        """
        },
    {
        "id": "doc6",
        "title": "Preparing for Scholarship Interviews",
        "content": """
        Many prestigious scholarships require interviews. Here's how to prepare:

        1. Research the scholarship organization thoroughly
        2. Practice common interview questions with a friend or mentor
        3. Prepare concrete examples of your achievements and challenges
        4. Dress professionally and arrive early
        5. Bring extra copies of your resume and application materials
        6. Prepare thoughtful questions to ask the interviewers
        7. Practice maintaining eye contact and positive body language
        8. Be prepared to discuss your future goals and career plans
        9. Show enthusiasm for your field of study and the scholarship
        10. Send a thank-you note within 24 hours after the interview

        Remember that interviews assess not just your achievements but also your personality and fit with the scholarship's values.
        """
    }
]

def retrieve_documents(query: str) -> List[Dict]:
    """
    Retrieve relevant documents based on query
    
    In a production environment, this would use a vector database or semantic search.
    This simplified version uses basic keyword matching.
    
    Args:
        query (str): Search query about scholarship concepts or tips
        
    Returns:
        List[Dict]: List of relevant document chunks
    """
    results = []
    query_terms = query.lower().split()
    
    for document in SCHOLARSHIP_DOCUMENTS:
        # Simple relevance scoring based on term frequency
        score = 0
        for term in query_terms:
            if term in document["title"].lower():
                score += 2  # Title matches are weighted higher
            if term in document["content"].lower():
                score += 1
        
        if score > 0:
            results.append({
                "id": document["id"],
                "title": document["title"],
                "content": document["content"],
                "relevance_score": score
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return results[:3]  # Return top 3 most relevant documents 