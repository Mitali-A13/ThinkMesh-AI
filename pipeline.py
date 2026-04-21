from dotenv import load_dotenv
from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

load_dotenv()


def run_research_pipeline(topic: str) -> dict:
    state = {
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "error": None,
        "status": "started",
    }

    try:
        # search agent working
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ]
            }
        )

        state["search_results"] = search_result["messages"][-1].content

        if not state["search_results"]:
            raise Exception("No search results found.")

        # reader agent working
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )

        state["scraped_content"] = reader_result["messages"][-1].content

        if not state["scraped_content"]:
            raise Exception("No scraped content returned.")

        # writer chain working
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke(
            {"topic": topic, "research": research_combined}
        )

        if not state["report"]:
            raise Exception("Report generation failed.")

        # critic chain working
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        state["status"] = "success"
        return state

    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state
