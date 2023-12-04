import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
// import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";


import {
  ErrorBoundary,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  // buildAutocompleteQueryConfig,
  // buildFacetConfigFromConfig,
  // buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig
  // getFacetFields
} from "./config/config-helper";

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200", // host url for the Elasticsearch instance
  index: "cv-transcriptions" // index name where the search documents are contained
});


const config = {
  searchQuery: {
    search_fields: {
      transcription: {}
    },
    result_fields: {
      file_path: {},
      duration: {},
      transcription: { snippet: {} }
    }
  },
  autocompleteQuery: {
    results: {
      resultsPerPage: 5,
      search_fields: {
        "transcription.suggest": {}
      }
    },
    result_fields: {
      transcription: {
        snippet: {}
      }
    }
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};



export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox autocompleteSuggestions={true} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort by"}
                          sortOptions={buildSortOptionsFromConfig()}
                        />
                      )}
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
