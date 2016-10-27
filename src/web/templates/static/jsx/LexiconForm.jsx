window.LexiconForm = React.createClass({

    onSubmit: function(e) {
        e.preventDefault();
        this.props.onSubmit();
    },

    onClear: function(e) {
        e.preventDefault();
        this.props.clearForm();
    },

    render: function() {
        var submitButtonText = this.props.isInProcessing ? 'Filtering ...' : 'Filter';

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
                            <input type="text" className="form-control" value={this.props.model.surface}
                                    onChange={this.props.changeField.bind(null, 'surface', false)}
                            />
                            <label style={{fontWeight: 'normal', color: 'gray'}}>
                                <input type="checkbox" checked={this.props.model.surface_is_regex}
                                        onChange={this.props.changeField.bind(null, 'surface_is_regex', true)}
                                />
                                <span> regex input </span>
                            </label>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="inputLemma" className="col-md-2 control-label">Lemma</label>
                        <div className="col-md-10">
                            <input type="text" className="form-control" value={this.props.model.lemma}
                                    onChange={this.props.changeField.bind(null, 'lemma', false)}
                            />
                            <label style={{fontWeight: 'normal', color: 'gray'}}>
                                <input type="checkbox" checked={this.props.model.lemma_is_regex}
                                        onChange={this.props.changeField.bind(null, 'lemma_is_regex', true)}
                                />
                                <span> regex input </span>
                            </label>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="inputMsd" className="col-md-2 control-label">Msd</label>
                        <div className="col-md-10">
                            <input type="text" className="form-control" value={this.props.model.msd}
                                    onChange={this.props.changeField.bind(null, 'msd', false)}
                            />
                            <label style={{fontWeight: 'normal', color: 'gray'}}>
                                <input type="checkbox" checked={this.props.model.msd_is_regex}
                                        onChange={this.props.changeField.bind(null, 'msd_is_regex', true)}
                                />
                                <span> regex input </span>
                            </label>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="inputNoOfSyllables" className="col-md-2 control-label">No of syllables</label>
                        <div className="col-md-10">
                            <input type="text" className="form-control" value={this.props.model.no_of_syllables}
                                    onChange={this.props.changeField.bind(null, 'no_of_syllables', false)}
                            />
                        </div>
                    </div>

                    <LanguagePicker options={this.props.languageOptions} selected={this.props.model.language}
                            onChange={this.props.changeField.bind(null, 'language', false)}/>

                    <div className="form-group">
                        <div className="col-md-10 col-md-offset-2">
                            <button className="btn btn-primary search-lexicon" onClick={this.onSubmit}
                                    disabled={this.props.isInProcessing}>
                                {submitButtonText}
                            </button>
                            <button className="btn btn-primary clear-lexicon" onClick={this.onClear}
                                    disabled={this.props.isInProcessing}>
                                Clear
                            </button>
                        </div>
                    </div>
                </fieldset>
            </form>
        )

    }
});