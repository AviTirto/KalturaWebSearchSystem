from typing import List
from piazza_api import Piazza
import json
from models import Answer, Question, Post
from pydantic import BaseModel

# Piazza login setup
p = Piazza()

# login method
def login():
    p.user_login("tirtosuharto@wisc.edu", "Kecap!2011")
    return p.get_user_classes()

# helper method for displaying user classes
def display_classes(user_classes):
    """Display the list of user classes for selection."""
    print("Available classes:")
    for idx, cls in enumerate(user_classes):
        print(f"{idx + 1}: {cls['name']} ({cls['term']})")
    print()

# helper method for picking classes
def pick_classes(user_classes):
    """Allow the user to pick classes by index."""
    display_classes(user_classes)
    selected_indices = input(
        "Enter the indices of classes to add to the database (comma-separated): "
    ).strip()
    
    try:
        indices = [int(idx) - 1 for idx in selected_indices.split(",")]
        selected_classes = [user_classes[idx] for idx in indices if 0 <= idx < len(user_classes)]
        return selected_classes
    except ValueError:
        print("Invalid input. Please enter valid indices.")
        return []

valid_posts = []
# method for adding posts to the database for a class
def add_to_db(cs_network):
    """Fetch and process posts from a selected class network."""
    for post in cs_network.iter_all_posts():
        print("Processing post:", post["nr"])
        try:
            if "history" not in post or not post["history"]:
                print("Skipping post due to missing or empty 'history':")
                # print(json.dumps(post, indent=4))
                continue
            
            question = post["history"][0]
            answers = post.get("children", [])

            if len(answers) == 0:
                continue

            has_instructor_answer = any(
                "type" in answer and answer["type"] == "i_answer" for answer in answers
            )
            has_instructor_endorsement = any(
                "tag_endorse" in answer and answer["tag_endorse"] for answer in answers
            )

            if has_instructor_answer or has_instructor_endorsement:
                question_obj = Question(
                    content=question["content"],
                    question_id=post["id"],
                    created=question["created"]
                )

                answer_objs = []
                for answer in answers:
                    if "history" not in answer or not answer["history"]:
                        print("Skipping answer due to missing or empty 'history':")
                        # print(json.dumps(answer, indent=4))
                        continue
                    
                    answer_history = answer["history"][0]
                    answer_obj = Answer(
                        content=answer_history["content"],
                        question_id=post["id"],
                        answer_id=answer["id"],
                        created=answer_history["created"],
                        tag=1 if answer.get("type") == "i_answer" else 0
                    )
                    answer_objs.append(answer_obj)

                post_obj = Post(
                    question=question_obj,
                    answers=answer_objs
                )
                print("Added post @" + str(post["nr"]))
                valid_posts.append(post_obj)

        except KeyError as e:
            print(f"KeyError occurred: {e}")
            print("Problematic post:")
            print(json.dumps(post, indent=4))
            continue

    print(f"Added {len(valid_posts)} valid posts to the database.")
    # for vp in valid_posts:
    #     print(vp.model_dump_json(indent=4))

# Main execution
user_classes = login()
selected_classes = pick_classes(user_classes)

for cls in selected_classes:
    print(f"Connecting to class: {cls['name']} ({cls['term']})")
    class_network = p.network(cls["nid"])
    add_to_db(class_network)


def pretty_print_pydantic(obj):
    """Pretty prints a Pydantic model instance."""
    print(json.dumps(obj.model_dump(), indent=4))

for vp in valid_posts:
    pretty_print_pydantic(vp)
