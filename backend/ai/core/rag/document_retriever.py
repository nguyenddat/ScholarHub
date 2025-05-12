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