USE capstone;
#DROP TABLE tblGame;
#DROP TABLE tblMovie;
#DROP TABLE tblReview;
#DROP TABLE tblTVShow
#SELECT COUNT(*) FROM tblReview;
#SELECT * FROM tblTVShow LIMIT 500, 10;
SELECT
	'tblGame' AS tbl,
    COUNT(*) FROM
tblGame

UNION

SELECT
	'tblMovie' AS tbl,
    COUNT(*) FROM
tblMovie

UNION

SELECT
	'tblTVShow' AS tbl,
    COUNT(*) FROM
tblTVShow

UNION

SELECT
	'tblReview' AS tbl,
    COUNT(*) FROM
tblReview;