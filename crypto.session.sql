SELECT * FROM crypto_prices_wide ORDER BY fetched_at DESC;

SELECT COUNT(*) FROM crypto_prices_wide;

SELECT fetched_at,
       GREATEST(bitcoin, ethereum, cardano, solana, dogecoin) AS highest_price,
       CASE GREATEST(bitcoin, ethereum, cardano, solana, dogecoin)
            WHEN bitcoin  THEN 'bitcoin'
            WHEN ethereum THEN 'ethereum'
            WHEN cardano  THEN 'cardano'
            WHEN solana   THEN 'solana'
            WHEN dogecoin THEN 'dogecoin'
       END AS highest_coin,
       LEAST(bitcoin, ethereum, cardano, solana, dogecoin) AS lowest_price,
       CASE LEAST(bitcoin, ethereum, cardano, solana, dogecoin)
            WHEN bitcoin  THEN 'bitcoin'
            WHEN ethereum THEN 'ethereum'
            WHEN cardano  THEN 'cardano'
            WHEN solana   THEN 'solana'
            WHEN dogecoin THEN 'dogecoin'
       END AS lowest_coin
FROM crypto_prices_wide
ORDER BY fetched_at DESC
LIMIT 1;


