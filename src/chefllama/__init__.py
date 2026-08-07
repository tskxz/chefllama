from langchain.messages import HumanMessage

def main() -> None:
    config = {"configurable": {"thread_id", "1"}}

    response = agent.invoke(
        {
            "messages":[
                #TODO ser input do user aqui
                HumanMessage(content='Tenho restos de peito de frango e arroz, o que posso fazer?'),
            ]
        },
        config
    )

    print(response([messages][-1].content))

    
