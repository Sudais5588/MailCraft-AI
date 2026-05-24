import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="MailCraft AI",
    page_icon="📧",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.title("📧 MailCraft AI")
    st.write("AI Agent Engineering Project")

    st.divider()

    st.markdown("### Project Info")
    st.write("**Track:** AI Agent Engineering")
    st.write("**Challenge:** Automated Email Copywriter Pipeline")
    st.write("**Purpose:** Generate and evaluate professional sales email sequences.")

    st.divider()

    st.markdown("### Features")
    st.write("✅ Email sequence generation")
    st.write("✅ Campaign strategy")
    st.write("✅ Email quality scoring")
    st.write("✅ Spam-word checking")
    st.write("✅ Download generated emails")

    st.divider()

    st.caption("Built for SiteArche Virtual Hackathon")


# -----------------------------
# Email Analysis Function
# -----------------------------

def analyze_email(subject, body, cta):
    score = 100
    feedback = []

    spam_words = [
        "free", "guaranteed", "limited time", "urgent",
        "act now", "winner", "risk-free", "100%"
    ]

    if len(subject) < 20:
        score -= 10
        feedback.append("Subject line is too short.")
    elif len(subject) > 70:
        score -= 10
        feedback.append("Subject line is too long.")

    if cta.lower() not in body.lower():
        score -= 15
        feedback.append("Call-to-action is not clearly included in the email body.")

    word_count = len(body.split())

    if word_count < 60:
        score -= 10
        feedback.append("Email body is too short.")
    elif word_count > 180:
        score -= 10
        feedback.append("Email body is too long.")

    found_spam_words = []

    for word in spam_words:
        if word.lower() in body.lower() or word.lower() in subject.lower():
            found_spam_words.append(word)

    if found_spam_words:
        score -= len(found_spam_words) * 5
        feedback.append(f"Possible spam words found: {', '.join(found_spam_words)}")

    if score < 0:
        score = 0

    if not feedback:
        feedback.append("Email looks clear, professional, and well-structured.")

    return score, feedback


# -----------------------------
# Email Generation Functions
# -----------------------------

def generate_subject(product_name, email_type, tone):
    subjects = {
        "Awareness": f"Discover how {product_name} can help you grow",
        "Value": f"Why {product_name} is a smart choice for your goals",
        "Trust": f"See how {product_name} creates real value",
        "Offer": f"Ready to get started with {product_name}?",
        "Final Reminder": f"Final reminder to explore {product_name}"
    }

    if tone == "Urgent":
        return f"Do not miss this opportunity with {product_name}"
    elif tone == "Friendly":
        return f"Thought you might like {product_name}"
    elif tone == "Persuasive":
        return f"Transform your results with {product_name}"
    else:
        return subjects[email_type]


def generate_email_body(
    product_name,
    target_audience,
    email_goal,
    tone,
    email_type,
    key_benefit,
    cta,
    sender_name
):
    tone_intro = {
        "Professional": "We understand that making the right decision requires clarity, trust, and value.",
        "Friendly": "We know it can be difficult to find the right solution, so we wanted to make things easier for you.",
        "Persuasive": "The right solution can save time, improve results, and create better opportunities.",
        "Urgent": "Now is the right time to take action and move forward with confidence."
    }

    templates = {
        "Awareness": f"""
Hi,

Are you a {target_audience} looking to {email_goal}?

{product_name} is designed to help you move forward with a simple, practical, and result-focused approach.

{tone_intro[tone]}

One of the key benefits is: {key_benefit}

{cta}

Best regards,  
{sender_name}
""",

        "Value": f"""
Hi,

Many {target_audience} face challenges when trying to {email_goal}. The main issue is not always effort, but having the right system and guidance.

That is where {product_name} can help.

With {product_name}, you can focus on what matters most while improving your results step by step.

Key benefit: {key_benefit}

{cta}

Best regards,  
{sender_name}
""",

        "Trust": f"""
Hi,

Before choosing any solution, trust is important.

{product_name} is built for {target_audience} who want to {email_goal} without wasting time on confusing or complicated processes.

It provides a clear direction, practical support, and a better way to achieve your goal.

Main value: {key_benefit}

{cta}

Best regards,  
{sender_name}
""",

        "Offer": f"""
Hi,

This is a great time to take the next step.

If you are a {target_audience} and your goal is to {email_goal}, then {product_name} can help you start with more confidence.

You do not need to overthink the process. Start small, take action, and improve consistently.

Benefit: {key_benefit}

{cta}

Best regards,  
{sender_name}
""",

        "Final Reminder": f"""
Hi,

This is a final reminder to explore {product_name}.

If you are serious about your goal to {email_goal}, this can be a useful step forward.

{product_name} is created to support {target_audience} with a practical and easy-to-follow approach.

Key benefit: {key_benefit}

{cta}

Best regards,  
{sender_name}
"""
    }

    return templates[email_type]


def generate_sequence(
    product_name,
    target_audience,
    email_goal,
    tone,
    number_of_emails,
    key_benefit,
    cta,
    sender_name
):
    email_types = ["Awareness", "Value", "Trust", "Offer", "Final Reminder"]
    selected_types = email_types[:number_of_emails]

    sequence = []

    for index, email_type in enumerate(selected_types, start=1):
        subject = generate_subject(product_name, email_type, tone)

        body = generate_email_body(
            product_name,
            target_audience,
            email_goal,
            tone,
            email_type,
            key_benefit,
            cta,
            sender_name
        )

        sequence.append({
            "number": index,
            "type": email_type,
            "subject": subject,
            "body": body
        })

    return sequence


# -----------------------------
# Main App UI
# -----------------------------

st.title("📧 MailCraft AI")
st.markdown("### AI Email Copywriter Pipeline for Sales Email Sequences")

st.info(
    "MailCraft AI helps students, freelancers, startups, and small businesses generate professional sales email sequences from simple input."
)

st.divider()

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("## Product Details")

    product_name = st.text_input(
        "Product or Service Name",
        placeholder="Example: Python Mastery Course"
    )

    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: University students"
    )

    email_goal = st.text_input(
        "Email Goal",
        placeholder="Example: learn Python and build real-world projects"
    )

    key_benefit = st.text_input(
        "Key Benefit",
        placeholder="Example: practical coding skills with hands-on projects"
    )

with right_col:
    st.markdown("## Email Settings")

    tone = st.selectbox(
        "Select Email Tone",
        ["Professional", "Friendly", "Persuasive", "Urgent"]
    )

    number_of_emails = st.slider(
        "Number of Emails in Sequence",
        min_value=1,
        max_value=5,
        value=3
    )

    cta = st.text_input(
        "Call To Action",
        placeholder="Example: Enroll today and start learning"
    )

    sender_name = st.text_input(
        "Sender Name / Team Name",
        placeholder="Example: MailCraft AI Team"
    )

st.divider()

generate_button = st.button("🚀 Generate Email Sequence", use_container_width=True)

if generate_button:
    if not product_name or not target_audience or not email_goal or not key_benefit or not cta:
        st.error("Please fill all required fields before generating emails.")
    else:
        if not sender_name:
            sender_name = "MailCraft AI Team"

        sequence = generate_sequence(
            product_name,
            target_audience,
            email_goal,
            tone,
            number_of_emails,
            key_benefit,
            cta,
            sender_name
        )

        st.success("Email sequence generated successfully!")

        # -----------------------------
        # Campaign Strategy Section
        # -----------------------------

        st.markdown("## Campaign Strategy")

        strategy_col1, strategy_col2, strategy_col3 = st.columns(3)

        with strategy_col1:
            st.metric("Target Audience", target_audience)

        with strategy_col2:
            st.metric("Selected Tone", tone)

        with strategy_col3:
            st.metric("Emails Generated", number_of_emails)

        st.markdown("### Recommended Campaign Approach")

        if tone == "Professional":
            st.write(
                "This campaign uses a clear and professional communication style. "
                "It focuses on trust, value, and practical benefits for the audience."
            )
        elif tone == "Friendly":
            st.write(
                "This campaign uses a warm and conversational tone. "
                "It is designed to build comfort and make the message feel personal."
            )
        elif tone == "Persuasive":
            st.write(
                "This campaign uses benefit-driven language to convince the audience. "
                "It highlights outcomes, value, and action."
            )
        else:
            st.write(
                "This campaign uses a time-sensitive tone. "
                "It encourages the audience to take action quickly while staying professional."
            )

        st.markdown("### Sequence Structure")
        st.write(
            "The generated campaign follows a step-by-step sales sequence: "
            "Awareness → Value → Trust → Offer → Final Reminder."
        )

        st.divider()

        # -----------------------------
        # Generated Emails Section
        # -----------------------------

        st.markdown("## Generated Email Sequence")

        full_output = f"""
MailCraft AI - Generated Email Sequence
Generated on: {datetime.now().strftime("%d %B %Y, %I:%M %p")}

Product/Service: {product_name}
Target Audience: {target_audience}
Goal: {email_goal}
Tone: {tone}
Number of Emails: {number_of_emails}

Campaign Strategy:
This campaign follows a structured sales sequence using the selected tone and audience details.

----------------------------------------
"""

        total_score = 0

        for email in sequence:
            score, feedback = analyze_email(email["subject"], email["body"], cta)
            total_score += score

            with st.expander(f"Email {email['number']} - {email['type']}", expanded=True):
                st.markdown(f"**Subject:** {email['subject']}")

                st.markdown(f"**Email Quality Score:** {score}/100")

                if score >= 80:
                    st.success("Strong email quality")
                elif score >= 60:
                    st.warning("Good, but can be improved")
                else:
                    st.error("Needs improvement")

                with st.expander("View Email Feedback"):
                    for item in feedback:
                        st.write(f"- {item}")

                st.markdown("**Email Body:**")

                st.text_area(
                    label=f"Email {email['number']} Body",
                    value=email["body"],
                    height=260,
                    key=f"email_body_{email['number']}"
                )

            full_output += f"""

Email {email['number']} - {email['type']}
Subject: {email['subject']}
Quality Score: {score}/100

{email['body']}

Feedback:
{chr(10).join(['- ' + item for item in feedback])}

----------------------------------------
"""

        average_score = total_score / len(sequence)

        st.markdown("## Overall Campaign Score")

        st.metric(
            label="Average Email Quality Score",
            value=f"{average_score:.1f}/100"
        )

        if average_score >= 80:
            st.success("This is a strong email campaign.")
        elif average_score >= 60:
            st.warning("This campaign is good, but it can be improved.")
        else:
            st.error("This campaign needs improvement.")

        st.download_button(
            label="⬇️ Download Email Sequence",
            data=full_output,
            file_name="mailcraft_email_sequence.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.markdown("## How MailCraft AI Works")

    st.write(
        "MailCraft AI takes your product details, target audience, email goal, tone, "
        "and call-to-action. Then it generates a structured sales email sequence."
    )

    st.markdown("### Pipeline")

    st.write("1. User enters product and campaign details")
    st.write("2. System selects email sequence structure")
    st.write("3. Email subjects and bodies are generated")
    st.write("4. Each email is analyzed using quality checks")
    st.write("5. Final email campaign can be downloaded")

    st.markdown("### Email Sequence Types")

    st.write("- Awareness Email")
    st.write("- Value Email")
    st.write("- Trust Email")
    st.write("- Offer Email")
    st.write("- Final Reminder Email")