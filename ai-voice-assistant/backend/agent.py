from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext, 
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv
from api import AssistantFnc
from prompts import WELCOME_MESSAGE, INSTRUCTIONS, LOOKUP_VIN_MESSAGE
import os

#ability to access keys for livekit
load_dotenv()

async def entrypoint(ctx: JobContext):
    #connects to livekit room - video, audio and text tracks
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,
        voice="shimmer",
        temperature=0.8,
        modalities=["audio", "text"]
    )
    #give an ai model access to various tools that can call and utilize
    assistant_fnc = AssistantFnc()
    #creating an agent
    assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
    
    #assistant joins room 
    assistant.start(ctx.room)
    #new session 
    session = model.sessions[0]
    #new conversation item
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content=WELCOME_MESSAGE
        )
    )
    #reads conversation item and responds - voice response
    session.response.create()

    #once user finishes talking the function below will trigger 
    @session.on("user_speech_committed")
    def on_user_speech_committed(msg: llm.ChatMessage):
        #convert message to string (could be a list or image)
        if isinstance(msg.content, list):
            msg.content = "\n".join("[image]" if isinstance(x, llm.ChatImage) else x for x in msg)
        
        #if user already has car info don't ask again
        if assistant_fnc.has_car():
            handle_query(msg)
        else:
            find_profile(msg)


    #response branches based on state
    #asks user for vin 
    def find_profile(msg: llm.ChatMessage):
        session.conversation.item.create(
            llm.ChatMessage(
                role="system",
                content=LOOKUP_VIN_MESSAGE(msg)
            )
        )
        session.response.create()

    #could continue branching with more questions - call another function within
    #gives car's make and model found with given vin 
    def handle_query(msg: llm.ChatMessage):
        session.conversation.item.create(
            llm.ChatMessage(
                role="user",
                content=msg.content
            )
        )
        session.response.create()
        

#call entry point function
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))