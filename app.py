import streamlit as st
from pdfminer.high_level import extract_text
from transformers import pipeline
import nltk
import io
import random

# Download NLTK punkt if not already present
nltk.download('punkt')

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("Smart Assistant for Research Summarization")

# File upload
uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])
text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        text = extract_text(uploaded_file)
    elif uploaded_file.type == "text/plain":
        # Extract text from TXT
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()
    st.success("File uploaded and text extracted!")
    st.write("---")
    st.subheader("Document Preview (first 500 chars):")
    st.write(text[:500])

    # Placeholder for summary
    st.subheader("Auto Summary")
    # Summarization logic
    if len(text) > 0:
        with st.spinner("Generating summary..."):
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            # Truncate or chunk text for summarization (Hugging Face models have max token limits)
            max_chunk = 1000  # characters per chunk
            text_chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
            summary = ""
            for chunk in text_chunks[:3]:  # Limit to first 3 chunks for performance and summary length
                out = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summary += out[0]['summary_text'] + " "
            # Limit summary to 150 words
            summary_words = summary.split()
            if len(summary_words) > 150:
                summary = ' '.join(summary_words[:150]) + '...'
            st.success("Summary generated!")
            st.write(summary)
    else:
        st.info("No text found to summarize.")

    # Placeholder for interaction modes
    st.subheader("Interaction Modes")
    st.markdown("**Ask Anything**: Ask any question about the uploaded document.")
    if len(text) > 0:
        user_question = st.text_input("Enter your question about the document:")
        if user_question:
            with st.spinner("Finding answer..."):
                qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
                # For long documents, use only the first 2000 characters for context (for demo/performance)
                context = text[:2000]
                result = qa_model(question=user_question, context=context)
                answer = result['answer']
                # Find the sentence containing the answer for justification
                from nltk.tokenize import sent_tokenize
                sentences = sent_tokenize(context)
                justification = next((s for s in sentences if answer in s), "(Reference not found in preview)")
                st.success(f"**Answer:** {answer}")
                st.markdown(f"**Justification:** _{justification}_")
    else:
        st.info("Upload a document and ask a question to use this mode.")
    st.markdown("---")
    st.subheader("Challenge Me Mode")
    st.markdown("**Challenge Me**: Answer logic-based questions about the document and get evaluated feedback.")
    
    if len(text) > 0:
        # Generate questions when button is clicked
        if st.button("Generate Challenge Questions"):
            with st.spinner("Generating new logic-based questions..."):
                # Enhanced logic-based question generation with variety
                sentences = text.split('.')[:30]  # Use more sentences for variety
                questions = []
                correct_answers = []
                
                # Filter substantial sentences
                substantial_sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
                
                # Shuffle sentences for variety
                random.shuffle(substantial_sentences)
                
                # Ensure we generate exactly 3 questions
                question_count = 0
                
                # Define different question types for variety
                question_types = [
                    "cause_effect",
                    "comparison", 
                    "inference",
                    "analysis",
                    "evaluation",
                    "synthesis"
                ]
                
                # Shuffle question types for variety
                random.shuffle(question_types)
                
                if len(substantial_sentences) >= 3:
                    # Question 1: Dynamic type based on shuffled types
                    if question_count < 3 and len(substantial_sentences) > 0:
                        sentence1 = substantial_sentences[0]
                        words1 = sentence1.split()
                        if len(words1) > 8:
                            question_type = question_types[0]
                            
                            if question_type == "cause_effect":
                                # Look for cause-effect indicators
                                cause_indicators = ['because', 'due to', 'as a result', 'therefore', 'consequently', 'leads to', 'causes']
                                effect_indicators = ['result', 'outcome', 'impact', 'effect', 'consequence']
                                
                                has_cause_effect = any(indicator in sentence1.lower() for indicator in cause_indicators + effect_indicators)
                                
                                if has_cause_effect:
                                    question = f"Based on the document, what is the logical relationship between the main concepts mentioned in this statement: '{sentence1[:100]}...'?"
                                else:
                                    question = f"What logical cause-and-effect relationship can be identified in this statement: '{sentence1[:100]}...'?"
                            
                            elif question_type == "comparison":
                                # Look for comparison indicators
                                comparison_indicators = ['however', 'but', 'while', 'whereas', 'compared to', 'unlike', 'similar to', 'different from']
                                
                                has_comparison = any(indicator in sentence1.lower() for indicator in comparison_indicators)
                                
                                if has_comparison:
                                    question = f"What logical comparison or contrast is being made in this statement: '{sentence1[:100]}...'?"
                                else:
                                    key_terms = [w for w in words1 if len(w) > 4][:2]
                                    question = f"How do the concepts of '{' and '.join(key_terms)}' relate to each other logically in the context of this document?"
                            
                            elif question_type == "inference":
                                question = f"What logical inference can be drawn from this statement: '{sentence1[:100]}...'?"
                            
                            elif question_type == "analysis":
                                question = f"How does this statement contribute to the overall logical structure of the document: '{sentence1[:100]}...'?"
                            
                            elif question_type == "evaluation":
                                question = f"What logical strengths or weaknesses can be identified in this statement: '{sentence1[:100]}...'?"
                            
                            else:  # synthesis
                                question = f"How does this statement logically connect to the broader themes in the document: '{sentence1[:100]}...'?"
                            
                            questions.append(question)
                            correct_answers.append(f"Analysis should focus on: {sentence1}")
                            question_count += 1
                    
                    # Question 2: Different type and sentence
                    if question_count < 3 and len(substantial_sentences) > 1:
                        sentence2 = substantial_sentences[1]
                        words2 = sentence2.split()
                        if len(words2) > 6:
                            question_type = question_types[1] if len(question_types) > 1 else question_types[0]
                            
                            if question_type == "cause_effect":
                                question = f"What logical consequences or implications can be derived from this statement: '{sentence2[:100]}...'?"
                            
                            elif question_type == "comparison":
                                question = f"What logical similarities or differences are implied in this statement: '{sentence2[:100]}...'?"
                            
                            elif question_type == "inference":
                                question = f"Based on this statement, what logical conclusion can be reached: '{sentence2[:100]}...'?"
                            
                            elif question_type == "analysis":
                                question = f"What logical reasoning is demonstrated in this statement: '{sentence2[:100]}...'?"
                            
                            elif question_type == "evaluation":
                                question = f"What logical criteria or standards are suggested by this statement: '{sentence2[:100]}...'?"
                            
                            else:  # synthesis
                                question = f"How does this statement logically integrate with the document's main argument: '{sentence2[:100]}...'?"
                            
                            questions.append(question)
                            correct_answers.append(f"Analysis should focus on: {sentence2}")
                            question_count += 1
                    
                    # Question 3: Different type and sentence
                    if question_count < 3 and len(substantial_sentences) > 2:
                        sentence3 = substantial_sentences[2]
                        words3 = sentence3.split()
                        if len(words3) > 5:
                            question_type = question_types[2] if len(question_types) > 2 else question_types[0]
                            
                            if question_type == "cause_effect":
                                question = f"What logical chain of reasoning connects this statement to the document's conclusions: '{sentence3[:100]}...'?"
                            
                            elif question_type == "comparison":
                                question = f"What logical framework is established by this statement in relation to other parts of the document: '{sentence3[:100]}...'?"
                            
                            elif question_type == "inference":
                                question = f"What logical implications can be extrapolated from this statement: '{sentence3[:100]}...'?"
                            
                            elif question_type == "analysis":
                                question = f"How does this statement logically support or challenge the document's main thesis: '{sentence3[:100]}...'?"
                            
                            elif question_type == "evaluation":
                                question = f"What logical validity or reliability can be assessed from this statement: '{sentence3[:100]}...'?"
                            
                            else:  # synthesis
                                question = f"How does this statement logically contribute to the overall coherence of the document: '{sentence3[:100]}...'?"
                            
                            questions.append(question)
                            correct_answers.append(f"Analysis should focus on: {sentence3}")
                            question_count += 1
                
                # If we couldn't generate enough logic-based questions, create diverse analytical ones
                analytical_questions = [
                    "What is the logical structure of the main argument presented in this document?",
                    "How do the different sections of this document logically connect to support the central thesis?",
                    "What logical assumptions underlie the conclusions drawn in this document?",
                    "How does the methodology described logically lead to the findings presented?",
                    "What logical gaps or limitations exist in the reasoning presented in this document?",
                    "How do the evidence and conclusions logically support each other in this document?",
                    "What logical framework guides the organization of ideas in this document?",
                    "How does the logical flow of the document contribute to its persuasiveness?",
                    "What logical counterarguments could be raised against the main points in this document?",
                    "How does the logical coherence of the document affect its overall effectiveness?"
                ]
                
                # Shuffle analytical questions for variety
                random.shuffle(analytical_questions)
                
                while question_count < 3:
                    questions.append(analytical_questions[question_count])
                    correct_answers.append("(Answer should analyze the logical structure and reasoning in the document)")
                    question_count += 1
                
                # Store in session state for display
                st.session_state.challenge_questions = questions
                st.session_state.correct_answers = correct_answers
        
        # Display questions and collect answers
        if 'challenge_questions' in st.session_state and st.session_state.challenge_questions:
            st.success("New Challenge Questions Generated!")
            
            # Add Generate New Questions button
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 Generate New Questions"):
                    del st.session_state.challenge_questions
                    del st.session_state.correct_answers
                    st.rerun()
            
            user_answers = []
            for i, question in enumerate(st.session_state.challenge_questions):
                st.markdown(f"**Question {i+1}:** {question}")
                answer = st.text_area(f"Your answer for question {i+1}:", key=f"answer_{i}")
                user_answers.append(answer)
            
            if st.button("Submit Answers for Evaluation"):
                st.subheader("Evaluation Results")
                
                for i, (question, user_answer, correct_answer) in enumerate(zip(
                    st.session_state.challenge_questions, 
                    user_answers, 
                    st.session_state.correct_answers
                )):
                    st.markdown(f"**Question {i+1}:** {question}")
                    st.markdown(f"**Your Answer:** {user_answer}")
                    
                    # Enhanced evaluation logic for logic-based questions
                    if user_answer.strip():
                        # Check for logical reasoning indicators
                        logic_indicators = [
                            'because', 'therefore', 'consequently', 'as a result', 'due to',
                            'leads to', 'implies', 'suggests', 'indicates', 'shows that',
                            'logically', 'reasoning', 'analysis', 'conclusion', 'inference',
                            'relationship', 'connection', 'cause', 'effect', 'impact',
                            'compare', 'contrast', 'however', 'while', 'whereas'
                        ]
                        
                        # Count logical reasoning words
                        user_words = user_answer.lower().split()
                        logic_word_count = sum(1 for word in user_words if word in logic_indicators)
                        
                        # Check if answer contains key words from the correct answer
                        correct_words = set(correct_answer.lower().split())
                        user_words_set = set(user_words)
                        overlap = len(correct_words.intersection(user_words_set))
                        
                        # Enhanced scoring system
                        score = 0
                        if logic_word_count >= 2:
                            score += 2  # Good logical reasoning
                        if overlap > 3:
                            score += 2  # Good content alignment
                        if len(user_answer.split()) > 15:
                            score += 1  # Sufficient detail
                        
                        # Evaluation based on score
                        if score >= 4:
                            st.success("✅ **Excellent logic-based answer!** Your response demonstrates strong analytical thinking and logical reasoning.")
                        elif score >= 2:
                            st.success("✅ **Good logic-based answer!** Your response shows logical reasoning and aligns with the document content.")
                        elif score >= 1:
                            st.warning("⚠️ **Partial logic-based answer.** Consider including more logical reasoning and analytical thinking.")
                        else:
                            st.warning("⚠️ **Basic answer.** Try to include logical reasoning and analytical connections.")
                        
                        st.markdown(f"**Reference from document:** _{correct_answer}_")
                        
                        # Provide specific feedback
                        if logic_word_count < 2:
                            st.info("💡 **Tip:** Try using logical connectors like 'because', 'therefore', 'consequently' to strengthen your reasoning.")
                    else:
                        st.error("❌ **No answer provided.**")
                    
                    st.markdown("---")
                
                st.info("💡 **Tip:** All answers should be based on the uploaded document content.")
        else:
            st.info("Click 'Generate Challenge Questions' to start the challenge!")
    else:
        st.info("Upload a document to use Challenge Me mode.")
else:
    st.info("Please upload a PDF or TXT document to get started.") 