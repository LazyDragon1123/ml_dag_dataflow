CREATE TABLE documents (
	document_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	ml_response varchar
);

CREATE TABLE parsed_total (
	business_id integer PRIMARY KEY NOT NULL,
	num_data integer,
	total real,
	ai_score real,
	ocr_score real,
	bbox varchar
);