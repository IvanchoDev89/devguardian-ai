<?php

return [
    'api' => [
        'driver' => 'database',
        'table' => 'rate_limit_records',
        'expire' => 60,
    ],
    
    // Custom rate limiters
    'login' => [
        'driver' => 'database',
        'table' => 'rate_limit_records',
        'expire' => 300, // 5 minutes
        'max_attempts' => 5,
    ],
    
    'scan' => [
        'driver' => 'database',
        'table' => 'rate_limit_records',
        'expire' => 60,
        'max_attempts' => 10,
    ],
    
    'admin' => [
        'driver' => 'database',
        'table' => 'rate_limit_records',
        'expire' => 60,
        'max_attempts' => 30,
    ],
];
