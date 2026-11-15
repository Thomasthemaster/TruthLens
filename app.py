import json
import os
import random
import streamlit as st

st.set_page_config(
    page_title="TruthLens",
    page_icon="🔎",
    layout="wide"
)

# =====================================================
# GAME DATA
# All training scenarios are fictional.
# =====================================================

LEVELS = [
    {
        "name": "Rookie",
        "difficulty": "Beginner",
        "xp": 10,
        "cases": [
            {
                "id": "rookie_1",
                "title": "The Library Mystery",
                "claim": "Clearview's public library closes at 6 PM today.",
                "evidence": [
                    ("Official library website",
                     "Updated today: today's closing time is listed as 6 PM."),
                    ("Library events calendar",
                     "A children's reading event is scheduled for next Wednesday."),
                    ("Official library announcement",
                     "Today's normal operating hours remain unchanged."),
                    ("Library social media",
                     "The library recently posted a photo of its new reading room.")
                ],
                "answer": "Supported",
                "explanation": (
                    "The official website directly lists today's closing time "
                    "as 6 PM. The official announcement confirms normal hours. "
                    "The reading event and reading-room photo are unrelated."
                ),
                "hints": [
                    "Find the evidence that mentions today's library hours.",
                    "The library website and official announcement are more "
                    "relevant than the events calendar.",
                    "Both official sources confirm that today's closing time is 6 PM."
                ]
            },
            {
                "id": "rookie_2",
                "title": "The Missing Pool",
                "claim": "Clearview's public swimming pool is closed all weekend.",
                "evidence": [
                    ("Viral social media post",
                     "An account claims the pool will be closed Saturday and Sunday, "
                     "but gives no source."),
                    ("City recreation department",
                     "An official announcement published today confirms the pool "
                     "will remain open Saturday and Sunday."),
                    ("Local weather report",
                     "The forecast predicts cloudy skies on Saturday morning."),
                    ("Pool schedule",
                     "The official schedule lists normal weekend operating hours.")
                ],
                "answer": "Contradicted",
                "explanation": (
                    "The official recreation department and pool schedule show "
                    "that the pool is open. The viral post conflicts with the "
                    "stronger available evidence."
                ),
                "hints": [
                    "Look for a source that directly discusses the pool's weekend hours.",
                    "Compare the viral post with the official recreation department.",
                    "The official announcement says the pool will remain open."
                ]
            }
        ]
    },
    {
        "name": "Investigator",
        "difficulty": "Easy",
        "xp": 20,
        "cases": [
            {
                "id": "investigator_1",
                "title": "The Great Game Study",
                "claim": "A headline says puzzle games make students 40% better at math.",
                "evidence": [
                    ("Fictional research survey",
                     "Students who regularly played puzzle games reported higher "
                     "average math scores than students who did not."),
                    ("Study methodology",
                     "Researchers did not randomly assign students to play games. "
                     "Previous math ability and study time were not controlled."),
                    ("School newsletter",
                     "The school announced a new art competition for next month."),
                    ("Research conclusion",
                     "The findings showed an association, not proof that gaming "
                     "caused higher scores."),
                    ("Student interview",
                     "One student said puzzle games are fun and challenging.")
                ],
                "answer": "Misleading",
                "explanation": (
                    "The survey found an association between gaming and math scores, "
                    "but it did not prove that games caused improvement. The headline "
                    "makes a stronger claim than the research supports."
                ),
                "hints": [
                    "Pay attention to the difference between students reporting "
                    "higher scores and games actually causing those scores.",
                    "Check the study methodology. Were other possible explanations controlled?",
                    "The research conclusion explicitly says it found an association, "
                    "not proof of cause and effect."
                ]
            },
            {
                "id": "investigator_2",
                "title": "The Disappearing Trees",
                "claim": "A post claims Clearview removed 500 trees from its central park this month.",
                "evidence": [
                    ("Anonymous online post",
                     "The post includes a photograph of several tree stumps and "
                     "claims 500 trees were removed."),
                    ("City parks department report",
                     "The latest report records that 12 diseased trees were removed "
                     "from central park this month."),
                    ("Photograph metadata",
                     "The photograph was originally uploaded three years ago. "
                     "Its location is not verified."),
                    ("Community calendar",
                     "A gardening workshop is planned for next Saturday."),
                    ("Parks department budget",
                     "The department recently approved funding for new walking paths.")
                ],
                "answer": "Contradicted",
                "explanation": (
                    "The official report records 12 removals, not 500. The photograph "
                    "is also old and does not establish that 500 trees were removed "
                    "this month."
                ),
                "hints": [
                    "Check whether the photograph actually proves the number of trees removed.",
                    "Look at the date and location of the photograph, then compare "
                    "the claim with the city report.",
                    "The current official report says 12 trees were removed, not 500."
                ]
            }
        ]
    },
    {
        "name": "Analyst",
        "difficulty": "Intermediate",
        "xp": 35,
        "cases": [
            {
                "id": "analyst_1",
                "title": "The Amazing Water Filter",
                "claim": "A headline claims a new filter removes 100% of harmful substances from drinking water.",
                "evidence": [
                    ("Manufacturer advertisement",
                     "The company claims its filter removes 100% of tested particles "
                     "in a laboratory demonstration."),
                    ("Independent laboratory report",
                     "An independent test found that the filter removed 96% of one "
                     "tested substance. Several other substances were not tested."),
                    ("Product reviews",
                     "Customers praised the filter's compact design and quiet operation."),
                    ("Testing conditions",
                     "The manufacturer's demonstration used a limited set of substances "
                     "under controlled conditions, not every possible contaminant."),
                    ("Company social media",
                     "The company recently announced a new product color."),
                    ("Product manual",
                     "The manual recommends replacing the filter every three months.")
                ],
                "answer": "Misleading",
                "explanation": (
                    "The headline suggests the filter removes every harmful substance. "
                    "But the independent test only measured certain substances and "
                    "did not support a 100% removal claim."
                ),
                "hints": [
                    "Compare what the advertisement promises with what the independent "
                    "test actually measured.",
                    "Notice that the independent test examined only one substance.",
                    "The evidence does not establish 100% removal of every harmful "
                    "substance. The headline overgeneralizes limited testing."
                ]
            },
            {
                "id": "analyst_2",
                "title": "The School Attendance Claim",
                "claim": "A report claims that a new school breakfast program increased attendance by 25%.",
                "evidence": [
                    ("School district report",
                     "Attendance increased by 25% during the same semester that the "
                     "breakfast program was introduced."),
                    ("District attendance records",
                     "The report compares this semester with the previous semester, "
                     "but not with the same seasonal period in previous years."),
                    ("Weather records",
                     "The semester had fewer severe weather closures than the previous semester."),
                    ("Breakfast menu",
                     "The menu included oatmeal, fruit, and toast."),
                    ("District statement",
                     "The district says the program may have contributed to the increase, "
                     "but other factors were not ruled out."),
                    ("School sports calendar",
                     "Several schools held sports tournaments during the semester.")
                ],
                "answer": "Misleading",
                "explanation": (
                    "Attendance increased, but the comparison does not prove the "
                    "breakfast program caused the change. Fewer weather closures "
                    "and other factors may have contributed."
                ),
                "hints": [
                    "A statistic can be accurate without proving why something happened.",
                    "Look for other changes that could explain the attendance increase.",
                    "The district itself says other factors were not ruled out. "
                    "The program's effect has not been proven."
                ]
            }
        ]
    },
    {
        "name": "Master Detective",
        "difficulty": "Advanced",
        "xp": 50,
        "cases": [
            {
                "id": "master_1",
                "title": "The Unsafe Bridge",
                "claim": "An anonymous account claims that a newly built bridge in Clearview is structurally unsafe.",
                "evidence": [
                    ("Anonymous social media account",
                     "The account says an engineer warned that the bridge could collapse, "
                     "but does not name the engineer or provide a report."),
                    ("City construction update",
                     "The city confirms construction was completed, but the update "
                     "does not include a structural inspection report."),
                    ("Local traffic report",
                     "Traffic near the bridge was heavier than usual on Tuesday."),
                    ("Photograph",
                     "A photograph shows a small surface mark on the bridge. Its age, "
                     "location, and cause are unknown."),
                    ("Independent engineering assessment",
                     "No independent inspection report or named expert assessment "
                     "is available in the evidence file."),
                    ("City events calendar",
                     "A community festival is scheduled near the bridge next month."),
                    ("Bridge opening announcement",
                     "The bridge opened to traffic two weeks ago.")
                ],
                "answer": "Unverified",
                "explanation": (
                    "The available evidence does not establish whether the bridge "
                    "is safe or unsafe. An anonymous claim and an unexplained "
                    "photograph are not enough. Unverified does NOT mean false."
                ),
                "hints": [
                    "Separate evidence that looks suspicious from evidence that "
                    "actually proves the claim.",
                    "The city confirms the bridge was built, but does that establish "
                    "whether it passed a structural inspection?",
                    "There is no inspection report or named expert assessment. "
                    "The claim cannot currently be confirmed or disproved."
                ]
            },
            {
                "id": "master_2",
                "title": "The Secret Health Discovery",
                "claim": "A viral article claims scientists have proven that a fictional fruit called Moonberry prevents all illnesses.",
                "evidence": [
                    ("Viral article",
                     "The article says a secret study proved Moonberry prevents every "
                     "known illness, but does not identify researchers or link to the study."),
                    ("Referenced research paper",
                     "The article links to a paper about antioxidant levels in a "
                     "different fruit. The paper does not mention Moonberry or disease prevention."),
                    ("Food science blog",
                     "A fictional food science blog explains that some fruits contain "
                     "nutrients that support normal body functions."),
                    ("Article publication details",
                     "The article has no author name, publication date, or editorial information."),
                    ("Independent research databases",
                     "No matching study supporting the Moonberry claim is identified "
                     "in the supplied evidence file."),
                    ("Advertisement",
                     "A banner on the article's website advertises a fictional Moonberry supplement."),
                    ("Website design",
                     "The article uses colorful graphics and a large headline.")
                ],
                "answer": "Unverified",
                "explanation": (
                    "The linked paper does not support the article's claim. The article "
                    "also lacks identifiable authorship and reliable research evidence. "
                    "This makes the claim unverified, not automatically false."
                ),
                "hints": [
                    "Check whether the linked paper actually studies Moonberry.",
                    "A source can link to a real research paper that does not support "
                    "the claim being made.",
                    "The cited paper is about a different fruit, and no matching "
                    "research is provided. The claim remains unverified."
                ]
            }
        ]
    }
]

ANSWERS = ["Supported", "Contradicted", "Misleading", "Unverified"]

# =====================================================
# SAVE / LOAD
# =====================================================

SAVE_FILE = "truthlens_progress.json"


def default_progress():
    return {
        "xp": 0,
        "completed_cases": [],
        "attempts": {},
        "current_case_id": None,
        "tutorial_completed": False
    }


def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            defaults = default_progress()
            defaults.update(data)

            # Ignore case IDs that no longer exist in this version.
            valid_ids = {
                case["id"]
                for level in LEVELS
                for case in level["cases"]
            }

            defaults["completed_cases"] = [
                case_id for case_id in defaults["completed_cases"]
                if case_id in valid_ids
            ]

            defaults["attempts"] = {
                case_id: count
                for case_id, count in defaults["attempts"].items()
                if case_id in valid_ids
            }

            if defaults["current_case_id"] not in valid_ids:
                defaults["current_case_id"] = None

            return defaults

        except (json.JSONDecodeError, OSError, TypeError):
            pass

    return default_progress()


def save_progress():
    data = {
        "xp": st.session_state.xp,
        "completed_cases": st.session_state.completed_cases,
        "attempts": st.session_state.attempts,
        "current_case_id": st.session_state.current_case_id,
        "tutorial_completed": st.session_state.tutorial_completed
    }

    # Write to a temporary file first to reduce the chance of a damaged save.
    temporary_file = SAVE_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    os.replace(temporary_file, SAVE_FILE)


# =====================================================
# INITIALIZE SESSION STATE
# =====================================================

if "progress_loaded" not in st.session_state:
    saved = load_progress()

    st.session_state.xp = saved["xp"]
    st.session_state.completed_cases = saved["completed_cases"]
    st.session_state.attempts = saved["attempts"]
    st.session_state.current_case_id = saved["current_case_id"]
    st.session_state.tutorial_completed = saved["tutorial_completed"]
    st.session_state.tutorial_step = 0
    st.session_state.tutorial_replay = False
    st.session_state.tutorial_answer = None
    st.session_state.feedback = ""
    st.session_state.rank_up_notice = ""
    st.session_state.progress_loaded = True


# =====================================================
# XP RANK SYSTEM
# Rank is calculated from XP, so it is automatically saved
# whenever the existing XP progress is saved.
# =====================================================

RANKS = [
    {"name": "Rookie", "emoji": "🔎", "xp": 0},
    {"name": "Field Investigator", "emoji": "🕵️", "xp": 50},
    {"name": "Evidence Analyst", "emoji": "📂", "xp": 150},
    {"name": "Master Detective", "emoji": "🎖️", "xp": 300},
    {"name": "Truth Guardian", "emoji": "🛡️", "xp": 500},
]


def get_rank_info(xp):
    """Return the player's current rank and progress to the next rank."""
    current_rank = RANKS[0]
    next_rank = None

    for index, rank in enumerate(RANKS):
        if xp >= rank["xp"]:
            current_rank = rank
            if index + 1 < len(RANKS):
                next_rank = RANKS[index + 1]

    if next_rank is None:
        return current_rank, None, 1.0, 0

    xp_into_rank = xp - current_rank["xp"]
    xp_needed = next_rank["xp"] - current_rank["xp"]
    progress = min(xp_into_rank / xp_needed, 1.0)
    remaining = max(next_rank["xp"] - xp, 0)

    return current_rank, next_rank, progress, remaining


# =====================================================
# GAME HELPERS
# =====================================================

def get_all_cases():
    return [
        case
        for level in LEVELS
        for case in level["cases"]
    ]


def get_next_case():
    for level in LEVELS:
        unfinished = [
            case for case in level["cases"]
            if case["id"] not in st.session_state.completed_cases
        ]

        if unfinished:
            return random.choice(unfinished)

    return None


def find_case(case_id):
    for level in LEVELS:
        for case in level["cases"]:
            if case["id"] == case_id:
                return case, level

    return None, None


def submit_answer(selected_answer, case, level):
    case_id = case["id"]

    if case_id in st.session_state.completed_cases:
        return

    attempts = st.session_state.attempts.get(case_id, 0) + 1
    st.session_state.attempts[case_id] = attempts

    if selected_answer == case["answer"]:

        old_rank, _, _, _ = get_rank_info(st.session_state.xp)

        st.session_state.xp += level["xp"]
        st.session_state.completed_cases.append(case_id)
        st.session_state.feedback = "correct"

        new_rank, _, _, _ = get_rank_info(st.session_state.xp)

        if new_rank["name"] != old_rank["name"]:
            st.session_state.rank_up_notice = (
                f"{new_rank['emoji']} RANK UP! You are now "
                f"{new_rank['name']}!"
            )
        else:
            st.session_state.rank_up_notice = ""

    else:

        # Penalty increases with each incorrect attempt:
        # 1st mistake: -3 XP
        # 2nd mistake: -5 XP
        # 3rd mistake: -7 XP
        # 4th+ mistake: -9 XP
        penalty = min(3 + (attempts - 1) * 2, 9)

        st.session_state.xp = max(
            0,
            st.session_state.xp - penalty
        )

        st.session_state.feedback = "incorrect"

    save_progress()


def go_to_academy():
    st.session_state.navigation = "Detective Academy"


# =====================================================
# NAVIGATION
# =====================================================

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Detective Academy"],
    key="navigation"
)


# =====================================================
# PLAYER STATS
# =====================================================

total_cases = len(get_all_cases())
completed_count = len(st.session_state.completed_cases)
current_rank, next_rank, rank_progress, xp_remaining = get_rank_info(
    st.session_state.xp
)

st.sidebar.divider()
st.sidebar.subheader("🏅 Player Rank")
st.sidebar.markdown(
    f"### {current_rank['emoji']} {current_rank['name']}"
)

if next_rank is not None:
    st.sidebar.progress(rank_progress)
    st.sidebar.caption(
        f"{xp_remaining} XP to {next_rank['name']}"
    )
else:
    st.sidebar.success("Maximum rank achieved!")

st.sidebar.subheader("⭐ Total XP")
st.sidebar.title(st.session_state.xp)

st.sidebar.progress(
    completed_count / total_cases if total_cases else 0
)

st.sidebar.caption(
    f"{completed_count} / {total_cases} cases completed"
)

st.sidebar.caption(
    "Progress is saved on this computer."
)


# =====================================================
# HOME PAGE
# =====================================================

if page == "Home":

    st.title("🔎 TruthLens")
    st.subheader("See beyond the headline.")

    st.write(
        "Learn to question information, investigate evidence, "
        "and verify confidently."
    )

    st.divider()

    st.subheader("🏅 Your Detective Rank")
    st.markdown(
        f"## {current_rank['emoji']} {current_rank['name']}"
    )

    if next_rank is not None:
        st.progress(rank_progress)
        st.caption(
            f"{xp_remaining} XP until {next_rank['emoji']} "
            f"{next_rank['name']}"
        )
    else:
        st.success("You've reached the highest rank: Truth Guardian!")

    left, right = st.columns(2)

    with left:
        st.header("🔍 Investigate")
        st.write(
            "Examine claims, evaluate sources, "
            "and explore supporting evidence."
        )
        st.info("Investigation mode is coming soon!")

    with right:
        st.header("🎓 Detective Academy")
        st.write(
            "Practice spotting misinformation through "
            "progressively harder investigative cases."
        )

        st.write(
            f"Your progress: {completed_count} / {total_cases} cases"
        )

        st.button(
            "Open Detective Academy",
            on_click=go_to_academy
        )

    st.divider()
    st.caption("TruthLens | Think critically. Verify confidently.")


# =====================================================
# DETECTIVE ACADEMY
# =====================================================

elif page == "Detective Academy":

    st.title("🎓 Detective Academy")

    st.write(
        "Every case tests your ability to separate useful evidence "
        "from distractions."
    )

    st.divider()

    # -------------------------------------------------
    # FIRST-TIME PLAYER TUTORIAL
    # This practice case is separate from the eight
    # official cases and never changes XP or attempts.
    # -------------------------------------------------

    if st.button("📘 Review Tutorial", key="review_tutorial"):
        st.session_state.tutorial_replay = True
        st.session_state.tutorial_step = 0
        st.session_state.tutorial_answer = None
        st.rerun()

    if not st.session_state.tutorial_completed or st.session_state.tutorial_replay:

        st.subheader("🧭 Detective Academy: Training Mission")
        st.caption("PRACTICE CASE — DOES NOT AFFECT YOUR XP OR OFFICIAL PROGRESS")

        tutorial_step = st.session_state.tutorial_step

        if tutorial_step == 0:
            st.markdown("### Welcome, detective!")
            st.write(
                "Before beginning the official investigations, let's practice "
                "how to examine a claim, inspect evidence, and choose a classification."
            )
            st.info(
                "There are four possible assessments: Supported, Contradicted, "
                "Misleading, and Unverified. Your job is to choose the one that "
                "best matches the evidence."
            )

            if st.button("Start Training ➜", key="tutorial_start"):
                st.session_state.tutorial_step = 1
                st.rerun()

        elif tutorial_step == 1:
            st.markdown("### Step 1: Read the claim")
            st.write(
                "A claim is a statement that someone wants you to believe. "
                "Your job is to check whether the evidence supports it."
            )
            st.info("The school permanently removed its garden.")
            st.write(
                "Do not decide yet. A claim is only the starting point of an investigation."
            )

            if st.button("Examine the Evidence ➜", key="tutorial_to_evidence"):
                st.session_state.tutorial_step = 2
                st.rerun()

        elif tutorial_step == 2:
            st.markdown("### Step 2: Examine the evidence")
            st.write(
                "Read each item and ask: Is it relevant? Is the source useful? "
                "Does it directly support or challenge the claim?"
            )

            with st.expander("Evidence 1: Official school announcement", expanded=True):
                st.write(
                    "The school announced that the garden is temporarily closed "
                    "for renovation. The plants have been moved to another section "
                    "of the campus and will return when the renovation is complete."
                )

            with st.expander("Evidence 2: Student photograph", expanded=True):
                st.write(
                    "A photograph shows an empty patch of soil where the garden "
                    "used to be. The photograph does not show what happened to the plants."
                )

            with st.expander("Evidence 3: School calendar", expanded=True):
                st.write(
                    "The school calendar lists a basketball tournament for next Friday. "
                    "This does not provide information about the garden."
                )

            st.warning(
                "Remember: a photograph can leave out context, and not every item "
                "in an evidence file is relevant."
            )

            if st.button("Make Your Assessment ➜", key="tutorial_to_answer"):
                st.session_state.tutorial_step = 3
                st.rerun()

        elif tutorial_step == 3:
            st.markdown("### Step 3: What is your assessment?")
            st.write("Choose the classification best supported by the evidence.")

            with st.form("tutorial_answer_form"):
                tutorial_answer = st.radio(
                    "Choose one:",
                    ANSWERS,
                    key="tutorial_answer_choice"
                )
                tutorial_submitted = st.form_submit_button("Submit Assessment")

            if tutorial_submitted:
                st.session_state.tutorial_answer = tutorial_answer
                st.session_state.tutorial_step = 4
                st.rerun()

        elif tutorial_step == 4:
            st.markdown("### Step 4: Training debrief")

            if st.session_state.tutorial_answer == "Contradicted":
                st.success("Correct! The evidence directly contradicts the claim.")
            else:
                st.info(
                    f"You selected **{st.session_state.tutorial_answer}**. "
                    "Let's examine why the best answer is **Contradicted**."
                )

            st.write(
                "The claim says the garden was permanently removed. However, "
                "the official school announcement says it is only temporarily closed "
                "for renovation and that the plants were moved to another campus section. "
                "That directly conflicts with the claim."
            )
            st.write(
                "**Why the other evidence matters:** The photograph shows only an "
                "empty patch and leaves out the plants' new location. The calendar "
                "entry is unrelated. Strong investigations consider context and relevance, "
                "not just whether a piece of evidence looks convincing."
            )
            st.info(
                "Quick guide: Supported = evidence backs the claim. "
                "Contradicted = reliable evidence conflicts with it. "
                "Misleading = some information may be true, but the claim twists or "
                "overstates it. Unverified = there is not enough reliable evidence "
                "to decide. Unverified does not mean false."
            )

            if st.button("Finish Training ➜", key="tutorial_to_graduation"):
                st.session_state.tutorial_step = 5
                st.rerun()

        elif tutorial_step == 5:
            st.balloons()
            st.success("🎓 Training complete! You're ready for the official cases.")
            st.write(
                "You practiced reading a claim, checking source relevance, "
                "considering context, and choosing an evidence-based classification."
            )
            st.write(
                "This tutorial did not award or deduct XP, and it did not count "
                "as one of your eight official cases."
            )

            if not st.session_state.tutorial_completed:
                st.session_state.tutorial_completed = True
                save_progress()

            if st.button("Enter Detective Academy ➜", key="tutorial_finish"):
                st.session_state.tutorial_replay = False
                st.session_state.tutorial_step = 0
                st.session_state.tutorial_answer = None
                st.rerun()

        # Keep the official cases hidden until the tutorial is complete.
        st.stop()

    # Pick a case if there isn't one already selected.
    if st.session_state.current_case_id is None:
        next_case = get_next_case()

        if next_case is not None:
            st.session_state.current_case_id = next_case["id"]
            save_progress()

    selected_case, selected_level = find_case(
        st.session_state.current_case_id
    )

    # -------------------------------------------------
    # ACADEMY COMPLETE
    # -------------------------------------------------

    if selected_case is None:

        st.balloons()
        st.success("🏆 Congratulations! You've completed the Academy!")

        st.metric("Total XP earned", st.session_state.xp)

        st.write(
            "You've completed every investigation and practiced "
            "evaluating claims using evidence."
        )

        if st.button("Play Academy Again"):

            st.session_state.xp = 0
            st.session_state.completed_cases = []
            st.session_state.attempts = {}
            st.session_state.current_case_id = None
            st.session_state.feedback = ""
            st.session_state.rank_up_notice = ""

            save_progress()
            st.rerun()

    # -------------------------------------------------
    # ACTIVE CASE
    # -------------------------------------------------

    else:

        level_index = LEVELS.index(selected_level)
        case_id = selected_case["id"]

        attempts = st.session_state.attempts.get(case_id, 0)

        st.subheader(
            f"Level {level_index + 1}: {selected_level['name']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Difficulty", selected_level["difficulty"])

        with col2:
            st.metric("Case Reward", f"+{selected_level['xp']} XP")

        with col3:
            st.metric(
                "Cases Completed",
                f"{completed_count} / {total_cases}"
            )

        st.progress(completed_count / total_cases)

        st.divider()

        st.subheader(f"🗂️ Case File: {selected_case['title']}")

        st.caption("TRAINING SCENARIO — ALL INFORMATION IS FICTIONAL")

        st.subheader("📰 The Claim")
        st.info(selected_case["claim"])

        st.subheader("🔎 Evidence Dossier")

        st.write(
            "Examine every source carefully. Some information may be "
            "irrelevant, outdated, incomplete, or less reliable."
        )

        for number, (source, detail) in enumerate(
            selected_case["evidence"], start=1
        ):

            with st.expander(
                f"Evidence {number}: {source}",
                expanded=True
            ):
                st.write(detail)

        st.divider()

        # -------------------------------------------------
        # CORRECT ANSWER FEEDBACK
        # -------------------------------------------------

        if st.session_state.feedback == "correct":

            st.success(
                f"Investigation successful! +{selected_level['xp']} XP ⭐"
            )

            if st.session_state.rank_up_notice:
                st.balloons()
                st.success(st.session_state.rank_up_notice)

            st.subheader("🧠 Case Debrief")
            st.write(selected_case["explanation"])

            st.info(
                "You can earn the reward for this case only once. "
                "Your completed case has been saved."
            )

            if st.button("Continue to Next Case ➜"):

                st.session_state.feedback = ""
                st.session_state.rank_up_notice = ""

                next_case = get_next_case()

                if next_case is None:
                    st.session_state.current_case_id = None
                else:
                    st.session_state.current_case_id = next_case["id"]

                save_progress()
                st.rerun()

        # -------------------------------------------------
        # ANSWERING / INCORRECT FEEDBACK
        # -------------------------------------------------

        else:

            if st.session_state.feedback == "incorrect":

                st.error("Not quite! Your assessment needs another look.")

                st.write(
                    "You lost XP for this attempt. Review the evidence "
                    "before trying again."
                )

                # Hints become more specific after each mistake.
                hint_index = min(
                    attempts - 1,
                    len(selected_case["hints"]) - 1
                )

                st.warning(
                    f"💡 Investigation hint {hint_index + 1}: "
                    f"{selected_case['hints'][hint_index]}"
                )

                next_penalty = min(3 + attempts * 2, 9)

                st.caption(
                    f"Incorrect attempts: {attempts} | "
                    f"Next incorrect answer costs {next_penalty} XP."
                )

            else:

                st.subheader("What's your assessment?")

                st.caption(
                    "Choose the classification best supported by the evidence."
                )

            with st.form(f"case_form_{case_id}"):

                selected_answer = st.radio(
                    "Choose the most accurate classification:",
                    ANSWERS
                )

                submitted = st.form_submit_button(
                    "Submit Investigation"
                )

            if submitted:

                submit_answer(
                    selected_answer,
                    selected_case,
                    selected_level
                )

                st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.sidebar.divider()
st.sidebar.caption("TruthLens | Think critically. Verify confidently.")
