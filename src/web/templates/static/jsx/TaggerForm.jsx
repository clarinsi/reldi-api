window.SearchForm = React.createClass({

    getInitialState: function() {
        return {
            taggerForm: {

            },
            lexiconForm: {

            }
        }
    },

    render: function() {
        return (
            <ReactBootstrap.Tabs defaultActiveKey={2} id="uncontrolled-tab-example" bsStyle="pills">
                <ReactBootstrap.Tab eventKey={1} title="Tagger">
                    <div className="col-md-5">
                        <form id="search-form" className="form-horizontal tab-pane fade in">
                            <fieldset>
                                <div className="bordered">
                                    <div className="form-group">
                                        <label htmlFor="input-text" className="col-md-2 control-label">Text</label>
                                        <div className="col-md-9 col-md-offset-2">
                                            <textarea className="form-control" rows="10" id="input-text" style={{border: '1px solid #E8E7E7'}}></textarea>
                                        </div>
                                    </div>
                                    <div className="separator"><span>or</span></div>
                                    <div className="form-group">
                                        <label htmlFor="input-text" className="col-md-2 control-label no-top-padding">File</label>
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
                                            <input type="radio" name="input-format" id="input-format-1" value="json" />
                                            Text
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="input-format" id="input-format-2" value="tcf" />
                                            TCF
                                        </label>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-md-2 control-label">Function</label>
                                    <div className="col-md-10">
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method1" value="tag" />
                                            Tag
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method2" value="lemmatise" />
                                            Lemmatise
                                        </label>
                                        <label className="radio-inline">
                                            <input type="radio" name="method" id="method3" value="tag_lemmatise" />
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
                    </div>
                    <div className="col-md-7">
                        <SearchFormResult />
                    </div>
                </ReactBootstrap.Tab>
                <ReactBootstrap.Tab eventKey={2} title="Lexicon">
                    <div className="col-md-5">
                        <form id="lexicon-form" className="form-horizontal tab-pane fade in">
                            <fieldset>
                                <div className="form-group">
                                    <div className="col-md-12" style={{backgroundColor: '#F7F7F7'}}>
                                        <ul className="list-group" style={{paddingLeft: '20px'}}>
                                            <h4>Parameter description</h4>
                                            <li><strong>Regular input: </strong>
                                                In addition to completely matching a string, you can use the special character %
                                                as a wildcard to match an arbitrary string, including an empty string
                                            </li>
                                            <strong>Examples:</strong>
                                            <ul>
                                                <li>pet% matches pet, petodnevni, peteročlan, petostran etc.</li>
                                                <li>%pet matches pet, napet, trepet, opet etc.</li>
                                                <li>%pet% matches any string containing the substring pet.</li>
                                            </ul>
                                            <li><strong>Regex input: </strong> all regular expression characters are allowed</li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="inputSurface" className="col-md-2 control-label">Surface</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputSurface" />
                                        <label style={{fontWeight: 'normal', color: 'gray'}}>
                                            <input type="checkbox" id="surface_is_regex" value="0" />
                                            <span> regex input </span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="inputLemma" className="col-md-2 control-label">Lemma</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputLemma" />
                                        <label style={{fontWeight: 'normal', color: 'gray'}}>
                                            <input type="checkbox" id="lemma_is_regex" value="0" />
                                            <span> regex input </span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="inputMsd" className="col-md-2 control-label">Msd</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputMsd" />
                                        <label style={{fontWeight: 'normal', color: 'gray'}}>
                                            <input type="checkbox" value="0" id="msd_is_regex" />
                                            <span> regex input </span>
                                        </label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="inputNoOfSyllables" className="col-md-2 control-label">No of syllables</label>
                                    <div className="col-md-10">
                                        <input type="text" className="form-control" id="inputNoOfSyllables" />
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
                    <div className="col-md-7">
                        <SearchFormResult />
                    </div>
                </ReactBootstrap.Tab>
            </ReactBootstrap.Tabs>
        )

    }
});