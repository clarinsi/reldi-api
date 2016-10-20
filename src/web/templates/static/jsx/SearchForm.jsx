SearchForm = React.createClass({

    render: function() {
        return (
            <ul className="nav nav-pills">
                <li className="active"><a data-toggle="tab" href="#search-form" id="search_link">Tagger</a></li>
                <li className=""><a data-toggle="tab" href="#lexicon-form" id="lexicon_link">Lexicon</a></li>
            </ul>
            <div className="col-md-5">
                <div className="bs-component">
                    <div className="tab-content">
                        <form id="search-form" className="form-horizontal tab-pane fade in active">
                            <fieldset>
                                <div className="bordered">
                                    <div className="form-group">
                                        <label for="input-text" className="col-md-2 control-label">Text</label>
                                        <div className="col-md-9 col-md-offset-2">
                                            <textarea className="form-control" rows="10" id="input-text" style="border: 1px solid #E8E7E7;"></textarea>
                                        </div>
                                    </div>
                                    <div className="separator"><span>or</span></div>
                                    <div className="form-group">
                                        <label for="input-text" className="col-md-2 control-label no-top-padding">File</label>
                                        <div className="col-md-7">
                                            <input id="tagger-file-chooser" type="file" name="input-file" />
                                        </div>
                                        <button id="remove-file" className="btn btn-primary btn-xs no-top-margin">remove</button>
                                    </div>
                                </div>


                                <div className="form-group">
                                    <label className="col-md-2 control-label">Format</label>
                                    <div className="col-md-10">
                                        <label className="radio-inline">
                                            <input type="radio" name="input-format" id="input-format-1" value="json">
                                            Text
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="input-format" id="input-format-2" value="tcf">
                                            TCF
                                        </label>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-md-2 control-label">Function</label>
                                    <div className="col-md-10">
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method1" value="tag">
                                            Tag
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method2" value="lemmatise">
                                            Lemmatise
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method3" value="tag_lemmatise">
                                            Tag  +  Lemmatise
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="col-md-10 col-md-offset-2">
                                        <button id="search-button" type="submit" className="btn btn-primary">Process</button>
                                        <button id="tagger-clear-button" type="submit" className="btn btn-primary clear-tag">Clear</button>
                                    </div>
                                </div>
                            </fieldset>
                        </form>
                        <form id="lexicon-form" className="form-horizontal tab-pane fade">
                            <fieldset>
                                <div className="form-group">
                                    <div className="col-md-12" style="background-color: #F7F7F7">
                                        <ul className="list-group" style="padding-left: 20px;">
                                            <h4>Parameter description</h4>
                                            <li><strong>Regular input:</strong>
                                                In addition to completely matching a string, you can use the special character %
                                                as a wildcard to match an arbitrary string, including an empty string
                                            </li>
                                            <ul><strong>Examples:</strong>
                                                <li>pet% matches pet, petodnevni, peteročlan, petostran etc.</li>
                                                <li>%pet matches pet, napet, trepet, opet etc.</li>
                                                <li>%pet% matches any string containing the substring pet.</li>
                                            </ul>
                                            <li><strong>Regex input:</strong> all regular expression characters are allowed</li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label for="inputSurface" className="col-md-2 control-label">Surface</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputSurface">
                                        <label style="font-weight: normal; color: gray">
                                            <input type="checkbox" id="surface_is_regex" value="0">
                                            <span>regex input</span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label for="inputLemma" className="col-md-2 control-label">Lemma</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputLemma">
                                        <label style="font-weight: normal; color: gray">
                                            <input type="checkbox" id="lemma_is_regex" value="0">
                                            <span>regex input</span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label for="inputMsd" className="col-md-2 control-label">Msd</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputMsd">
                                        <label style="font-weight: normal; color: gray">
                                            <input type="checkbox" value="0" id="msd_is_regex">
                                            <span>regex input</span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label for="inputNoOfSyllables" className="col-md-2 control-label">No of syllables</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputNoOfSyllables">
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="col-md-10 col-md-offset-2">
                                        <button id="lexicon-button" type="submit" className="btn btn-primary search-lexicon">Filter</button>
                                        <button id="lexicon-clear-button" type="submit" className="btn btn-primary clear-lexicon">Clear</button>
                                    </div>
                                </div>
                            </fieldset>
                        </form>
                    </div>
                </div>
            </div>
            <div className="col-md-7">
                <div className="form-group">
                    <label for="textArea" className="col-md-12 control-label">Result</label>
                    <ul className="nav nav-pills">
                        <li className="active"><a data-toggle="tab" href="#table-results">Table</a></li>
                        <li className=""><a data-toggle="tab" href="#raw-results">Raw</a></li>
                        <li className="">
                            <a id="download-result" href="{{ url_for('web_router.download', requestId='') }}" target="_blank" className="btn btn-default"
                                style="margin: 0; text-transform: none;">Download</a>
                        </li>
                    </ul>
                    <div className="bs-component">
                        <div className="tab-content">
                            <div id="table-results" className="form-horizontal tab-pane fade in active" >
                                <table id="results"  className="table" cellspacing="0" width="100%" ></table>
                                <div id="lexicon-results-wrapper">
                                    <table id="lexicon-results" className="table" cellspacing="0" width="100%" >
                                        <thead>
                                            <tr>
                                                <th>Surface</th>
                                                <th>Tags</th>
                                                <th>Lemma</th>
                                            </tr>
                                        </thead>
                                    </table>
                                </div>
                            </div>
                            <div id="raw-results" className="form-horizontal  tab-pane fade">
                                <div className="col-md-12">
                                    <textarea id="result-area" readonly="readonly" className="form-control" rows="20"></textarea>
                                    <textarea id="lexicon-result-area" readonly="readonly" className="form-control" rows="20"></textarea>
                                </div>
                            </div>
                            <div className="help-block">
                                Result set
                                <span id="response-time"></span>
                            </div>
                            <div id="error-message"></div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});