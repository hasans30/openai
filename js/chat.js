import { OpenAI } from "langchain/llms/openai";
import "dotenv/config";

const model = new OpenAI({
  openAIApiKey: process.env.OPENAI_API_KEY,
  model: "davinci",
  temperature: 0.9,
});

const res = await model.call(
  //   "What would be a good company name a company that makes colorful socks?"
  "how microsoft skype manages configuration?"
);
console.log(res);
