window.LexiconForm = React.createClass({

    render: function() {
        return (
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
        )

    }
});