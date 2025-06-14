#!/bin/bash

# Проверим, существует ли интерфейс wg0
if wg show wg0 > /dev/null 2>&1; then
    exit 0
else
    exit 1
fi