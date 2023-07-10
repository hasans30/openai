// import { Chroma } from "langchain/vectorstores/chroma";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAI } from "langchain/llms/openai";
import { RetrievalQAChain } from "langchain/chains";
import { TextLoader } from "langchain/document_loaders/fs/text";
import { DirectoryLoader } from "langchain/document_loaders/fs/directory";
import "dotenv/config";

const queryText = process.argv.slice(2).join(" ");
console.log(`searching for...`, queryText);

const loader = new DirectoryLoader("./new_articles/", {
  ".txt": (path) => new TextLoader(path),
});

const documents = await loader.load();

//splitting the text into
const text_splitter = new RecursiveCharacterTextSplitter();
text_splitter.chunkSize = 1000;
text_splitter.chunkOverlap = 200;

const texts = await text_splitter.splitDocuments(documents);

console.log("loaded text form directory (our knowledge db)", texts.length);

// here we are using OpenAI embeddings but in future we will swap out to local embeddings
const embedding = new OpenAIEmbeddings();

const vectorStore = await MemoryVectorStore.fromDocuments(documents, embedding);

// This is how to perform similarity search
/*
const resultOne = await vectorStore.similaritySearch("kalam", 1);
console.log(resultOne);
*/

const retriever = vectorStore.asRetriever();

const model = new OpenAI({
  modelName: "text-davinci-003",
  temperature: 0.9,
});

//use the model directly
const response = await model.call(queryText);
console.log(`calling model directly: ${response ?? "no answer returned"}`);

// model with retrival qa chain with personal knowledge base
const chain = RetrievalQAChain.fromLLM(model, retriever);
const res = await chain.call({
  query: queryText,
});
console.log({ res });
