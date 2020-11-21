'use strict';
const e = React.createElement;
const d = React.ReactDOM;

class Page {
	constructor(data) {
			this.number      = data.number;
			this.src         = data.src;
			this.title       = data.title;
			this.description = data.description;
			this.first       = data.first;
			this.last        = data.last;
	}
}

function navTo(n) {
	loadPage(n);
}


async function loadPage(n) {
	if (document.getElementById('root') && document.getElementById('root').children.length == 0 ) {
		let layout = [];
		layout.push( e('div', {className: 'pageWrap'}, e('div', {className: 'lds-dual-ring', id: 'spinner'})) );
		ReactDOM.render(layout, document.getElementById('root'));
	}

	let response = await fetch('http://zero-25.com/p/'+n, {method : 'post'}).then(x => x.json()).then(x => {
		if (x[0].response == 'good') {
			assemblePage(x[0].page);
		} else {
			alert('Not Available');
		}
	});
}

function assemblePage(data) {
	const page = new Page(data);
	let layout = [];
	layout.push(e('div', {className: 'pageWrap'},
		e('img', {src : page.src, onLoad: function() { if (document.getElementById('spinner')) {document.getElementById('spinner').remove()} }}), 
		e('h1', null, 'Page No. ' + page.number + ' "' + page.title + '"'), 
		e('div', {className: 'description'}, e('p', null, page.description)), 
		e('div',{className:'controls'}, 
		e('div',{className:'first', onClick: function() {navTo(page.first)}},
		e('i',{className:'fa fa-step-backward'})),
		e('div',{className:'prev', onClick: function() {navTo(page.number-1)}},
		e('i',{className:'fa fa-arrow-circle-left'})), 
		e('div',{className:'next', onClick: function() {navTo(page.number+1)}}, 
		e('i',{className:'fa fa-arrow-circle-right'})),
		e('div',{className:'last', onClick: function() {navTo(page.last)}},
		e('i',{className: 'fa fa-step-forward'})))));
	ReactDOM.render(layout, document.getElementById('root'));
	window.scrollTo(0,0);
}

