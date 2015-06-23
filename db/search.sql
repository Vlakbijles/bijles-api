query_offers = session.query("id", "user_id", "user_meta_name", "user_meta_surname", "no_reviews", "no_endorsed",
                             "user_meta_photo_id", "user_meta_city", "distance", "subject_name", "level_name").\
    from_statement(text("""
                        SELECT d.id, d.user_id, d.user_meta_name, d.user_meta_surname,
                               d.user_meta_photo_id, d.user_meta_city, d.distance, d.subject_name,
                               d.level_name,
                               COUNT(review.endorsed) as no_reviews,
                               COUNT(CASE WHEN review.endorsed THEN 1 END) AS no_endorsed
                        FROM (SELECT z.*, p.radius,
                                     p.distance_unit * DEGREES(ACOS(COS(RADIANS(p.latp))
                                                     * COS(RADIANS(z.lat))
                                                     * COS(RADIANS(p.lonp - z.lon))
                                                     + SIN(RADIANS(p.latp))
                                                     * SIN(RADIANS(z.lat)))) AS distance
                              FROM (SELECT offer.id AS id, user.id AS user_id,
                                         user_meta.latitude AS lat, user_meta.longitude AS lon,
                                         user_meta.name AS user_meta_name,
                                         user_meta.surname AS user_meta_surname,
                                         user_meta.city AS user_meta_city,
                                         user_meta.photo_id AS user_meta_photo_id,
                                         subject.name AS subject_name,
                                         level.name AS level_name
                                    FROM offer
                                    INNER JOIN user ON offer.user_id=user.id
                                    INNER JOIN level ON level.id=offer.level_id
                                    INNER JOIN subject ON subject.id=offer.subject_id
                                    INNER JOIN user_meta ON user.id=user_meta.user_id
                                    WHERE offer.subject_id = :subject_id
                                    AND offer.active = 1
                                    AND offer.level_id LIKE :level_id) AS z
                              INNER JOIN (SELECT  postal_code.lat AS latp, postal_code.lon AS lonp,
                                                  50.0 AS radius, 111.045 AS distance_unit
                                    FROM postal_code
                                    WHERE postal_code.postal_code_id = :postal_code) AS p ON 1=1
                              WHERE z.lat
                              BETWEEN p.latp - (p.radius / p.distance_unit)
                              AND p.latp + (p.radius / p.distance_unit)
                              AND z.lon
                              BETWEEN p.lonp - (p.radius / (p.distance_unit * COS(RADIANS(p.latp))))
                              AND p.lonp + (p.radius / (p.distance_unit * COS(RADIANS(p.latp))))
                              ) AS d
                        INNER JOIN offer ON offer.user_id = d.user_id
                        LEFT OUTER JOIN review
                        ON review.offer_id = offer.id
                        GROUP BY d.user_id
                        ORDER BY :order_by""")).params(postal_code=postal_code_to_id(offer_args['postal_code']),
                                                       subject_id=offer_args['subject'],
                                                       level_id=offer_args['level'],
                                                       order_by=offer_args['order_by'])
