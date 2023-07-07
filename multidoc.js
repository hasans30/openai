// import { Chroma } from "langchain/vectorstores/chroma";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAI } from "langchain/llms/openai";
import { RetrievalQAChain } from "langchain/chains";
import { TextLoader } from "langchain/document_loaders/fs/text";
import { DirectoryLoader } from "langchain/document_loaders/fs/directory";
import "dotenv/config";

// Load and process the text files
// const fileName = "c:\\tmp\\test.txt";
// const loader = new TextLoader(fileName);

const loader = new DirectoryLoader("./new_articles/", {
  ".txt": (path) => new TextLoader(path),
});

const documents = await loader.load();

//splitting the text into
const text_splitter = new RecursiveCharacterTextSplitter();
text_splitter.chunkSize = 1000;
text_splitter.chunkOverlap = 200;

//   (chunk_size = 1000),
//   (chunk_overlap = 200)
// );
// const texts = text_splitter.split_documents(documents);
const texts = await text_splitter.splitDocuments(documents);

console.log("loaded text form directory (our knowledge db)", texts.length);

// Embed and store the texts
// Supplying a persist_directory will store the embeddings on disk
const persistDirectory = "db";

// here we are using OpenAI embeddings but in future we will swap out to local embeddings
const embedding = new OpenAIEmbeddings();

const vectorStore = await MemoryVectorStore.fromDocuments(documents, embedding);

const resultOne = await vectorStore.similaritySearch("use support ticket", 1);
console.log(resultOne);
